from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Request
from sse_starlette.sse import EventSourceResponse
from core.security import get_api_key
from core.config import get_settings
from models.schemas import ScamMessageRequest, AgentResponse, FinalCallbackPayload
from services.ml_engine import MLEngine
from services.rule_engine import RuleEngine
from services.agent_controller import AgentController
from services.session_manager import SessionManager
from services.callback import send_final_result
from services.auth_service import get_current_user
from models.user import UserInDB
import json
import logging
from datetime import datetime

# Setup Logger
logger = logging.getLogger("scam_intel_api")

router = APIRouter(prefix="/api/v1", tags=["v1"])
settings = get_settings()

@router.get("/users/me", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user

# Initialize Services
# In production, use Dependency Injection or Lifespan for singletons
ml_engine = MLEngine()
rule_engine = RuleEngine()
session_manager = SessionManager()
agent_controller = AgentController()

@router.post("/process", response_model=AgentResponse)
async def process_message(
    request: ScamMessageRequest, 
    background_tasks: BackgroundTasks
):
    """
    Main endpoint to process incoming messages.
    """
    user_id = "public_guest" # Public Access by default
    
    # 1. Update Session History
    # 1. Analyze Message (Moved up)
    ml_score = ml_engine.predict(request.message.text)
    rule_score = rule_engine.analyze(request.message.text)
    risk_score = (0.5 * ml_score) + (0.5 * rule_score) 
    risk_percentage = round(risk_score * 100, 2)
    scam_detected = risk_percentage > 40
    
    # 2. Extract Intel & Batched Session Update
    extracted_intel = rule_engine.extract_entities(request.message.text)
    
    session = session_manager.update_session_batch(
        user_id, 
        request.sessionId, 
        message=request.message.model_dump(),
        new_intel=extracted_intel
    )

    # UPDATE STATS (Batched)
    stats_updates = {
        "total_messages": 1,
        "scams_detected": 1 if scam_detected else 0,
        "safe_messages": 0 if scam_detected else 1
    }
    
    # Add extracted entity counts
    if extracted_intel.get("bankAccounts"):
        stats_updates["bank_accounts_extracted"] = len(extracted_intel["bankAccounts"])
    if extracted_intel.get("upiIds"):
        stats_updates["upi_ids_extracted"] = len(extracted_intel["upiIds"])
    if extracted_intel.get("phishingLinks"):
        stats_updates["phishing_links_extracted"] = len(extracted_intel["phishingLinks"])
    if extracted_intel.get("phoneNumbers"):
        stats_updates["phone_numbers_extracted"] = len(extracted_intel["phoneNumbers"])
        
    session_manager.batch_update_stats(user_id, stats_updates)
    
    # Log Recent Activity for Dashboard
    activity_log = {
        "sessionId": request.sessionId,
        "snippet": request.message.text[:50] + "..." if len(request.message.text) > 50 else request.message.text,
        "timestamp": datetime.now().isoformat(),
        "status": "SCAM" if scam_detected else "SAFE",
        "riskScore": risk_percentage
    }
    session_manager.log_recent_activity(user_id, activity_log)
    
    # 4. Agent Response
    session = session_manager.get_session(user_id, request.sessionId)
    history = session.get("history", [])
    
    agent_reply = await agent_controller.generate_response(history, request.message.text)
    
    # 5. Check Lifecycle & Trigger Callback
    has_intel = any(len(v) > 0 for k, v in extracted_intel.items() if isinstance(v, list))
    
    if scam_detected and has_intel:
        # Get complete session intelligence
        session = session_manager.get_session(user_id, request.sessionId)
        current_intel = session.get("intelligence", {})
        
        # Ensure all required fields exist with proper names
        complete_intel = {
            "bankAccounts": current_intel.get("bankAccounts", []),
            "upiIds": current_intel.get("upiIds", []),
            "phishingLinks": current_intel.get("phishingLinks", []),
            "phoneNumbers": current_intel.get("phoneNumbers", []),
            "suspiciousKeywords": current_intel.get("suspiciousKeywords", [])
        }
        
        # Prepare Payload
        total_msgs = len(history) + 1  # +1 for current message
        
        callback_payload = {
            "sessionId": request.sessionId,
            "scamDetected": True,
            "totalMessagesExchanged": total_msgs,
            "extractedIntelligence": complete_intel,
            "agentNotes": f"Detected scam logic: ML={ml_score:.2f}, Rules={rule_score:.2f}. Risk={risk_percentage}%"
        }
        
        logger.info(f"🎯 Triggering callback with {sum(len(v) for v in complete_intel.values())} intelligence items")
        background_tasks.add_task(send_final_result, callback_payload)

    return AgentResponse(
        reply=agent_reply,
        riskScore=risk_percentage,
        scamDetected=scam_detected,
        extractedIntelligence=extracted_intel
    )

@router.get("/stats")
async def get_dashboard_stats():
    """
    Returns real-time global statistics for the Dashboard (User Scoped).
    """
    return session_manager.get_dashboard_stats("public_guest")

@router.post("/stream")
async def stream_message(
    request: ScamMessageRequest,
    background_tasks: BackgroundTasks
):
    """
    Streaming endpoint for chat. Yields tokens as Server-Sent Events.
    """
    # Public Access Mode
    user_id = "public_guest"
    
    # 1. Basic Analysis (Same as process, but lightweight)
    # We still need to extract intel and update session, but validation happens first
    
    async def event_generator():
        # A. Analyze & Update Stats
        # 1. Consolidated Session Update (Add Message + Update Intel)
        extracted_intel = rule_engine.extract_entities(request.message.text)
        
        # Restore Risk Analysis
        ml_score = ml_engine.predict(request.message.text)
        rule_score = rule_engine.analyze(request.message.text)
        risk_percentage = round(((0.5 * ml_score) + (0.5 * rule_score)) * 100, 2)
        scam_detected = risk_percentage > 40
        
        session = session_manager.update_session_batch(
            user_id, 
            request.sessionId, 
            message=request.message.model_dump(),
            new_intel=extracted_intel
        )

        # UPDATE STATS (Batched)
        stats_updates = {
            "total_messages": 1,
            "scams_detected": 1 if scam_detected else 0,
            "safe_messages": 0 if scam_detected else 1
        }
        
        # Add extracted entity counts
        if extracted_intel.get("bankAccounts"):
            stats_updates["bank_accounts_extracted"] = len(extracted_intel["bankAccounts"])
        if extracted_intel.get("upiIds"):
            stats_updates["upi_ids_extracted"] = len(extracted_intel["upiIds"])
        if extracted_intel.get("phishingLinks"):
            stats_updates["phishing_links_extracted"] = len(extracted_intel["phishingLinks"])
        if extracted_intel.get("phoneNumbers"):
            stats_updates["phone_numbers_extracted"] = len(extracted_intel["phoneNumbers"])
            
        session_manager.batch_update_stats(user_id, stats_updates)
        
        # Log Recent Activity for Dashboard
        activity_log = {
            "sessionId": request.sessionId,
            "snippet": request.message.text[:50] + "..." if len(request.message.text) > 50 else request.message.text,
            "timestamp": datetime.now().isoformat(),
            "status": "SCAM" if scam_detected else "SAFE",
            "riskScore": risk_percentage
        }
        session_manager.log_recent_activity(user_id, activity_log)
        
        # B. Send Metadata Event first
        metadata = {
            "riskScore": risk_percentage,
            "scamDetected": scam_detected,
            "extractedIntelligence": extracted_intel
        }
        yield {"event": "metadata", "data": json.dumps(metadata)}

        # C. Stream Agent Response
        # session object already updated in step 1
        history = session.get("history", [])
        
        logger.info(f"Generating response for session {request.sessionId}...")
        full_reply = ""
        token_count = 0
        try:
            logger.info(f"About to call generate_response_stream with history length: {len(history)}")
            async for chunk in agent_controller.generate_response_stream(history, request.message.text):
                token_count += 1
                if chunk:
                    logger.info(f"Router received chunk {token_count}: '{chunk}'")
                    full_reply += chunk
                    yield {"event": "token", "data": chunk}
                else:
                    logger.warning(f"Router received NULL chunk {token_count}")
            logger.info(f"Stream generation complete. Total tokens: {token_count}, Full reply length: {len(full_reply)}")
        except Exception as e:
            logger.error(f"Stream generation loop failed: {e}", exc_info=True)
            
        # D. Lifecycle Check - Trigger Callback
        has_intel = any(len(v) > 0 for k, v in extracted_intel.items() if isinstance(v, list))
        if scam_detected and has_intel:
            # Get complete session intelligence
            session_intel = session.get("intelligence", {})
            
            # Ensure all required fields with proper names
            complete_intel = {
                "bankAccounts": session_intel.get("bankAccounts", []),
                "upiIds": session_intel.get("upiIds", []),
                "phishingLinks": session_intel.get("phishingLinks", []),
                "phoneNumbers": session_intel.get("phoneNumbers", []),
                "suspiciousKeywords": session_intel.get("suspiciousKeywords", [])
            }
            
            payload = {
                "sessionId": request.sessionId,
                "scamDetected": True,
                "totalMessagesExchanged": len(history) + 1,
                "extractedIntelligence": complete_intel,
                "agentNotes": f"Stream: ML={ml_score:.2f}, Rules={rule_score:.2f}. Risk={risk_percentage}%"
            }
            
            logger.info(f"🎯 Triggering callback (stream) with {sum(len(v) for v in complete_intel.values())} items")
            await send_final_result(payload)

        # Final Event
        yield {"event": "end", "data": "DONE"}
    
    return EventSourceResponse(event_generator())

@router.get("/history")
async def get_chat_history(
    sessionId: str
):
    """
    Retrieve chat history for a specific session.
    """
    session = session_manager.get_session("public_guest", sessionId)
    return {
        "history": session.get("history", []),
        "intelligence": session.get("intelligence", {})
    }
