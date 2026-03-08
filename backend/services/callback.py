import httpx
import asyncio
import logging
from core.config import get_settings

settings = get_settings()
logger = logging.getLogger("scam_intel_callback")

# Required schema fields (MANDATORY for GUVI)
REQUIRED_FIELDS = [
    "sessionId",
    "scamDetected",
    "totalMessagesExchanged",
    "extractedIntelligence",
    "agentNotes"
]


async def send_final_result(payload: dict) -> bool:
    """
    Sends final intelligence payload to GUVI callback endpoint.
    Retries 3 times with exponential backoff.
    Returns True if successful, False otherwise.
    """

    url = settings.CALLBACK_URL

    # -------------------------------
    # 1️⃣ Validate Required Fields
    # -------------------------------
    for field in REQUIRED_FIELDS:
        if field not in payload:
            logger.error(f"❌ Missing required field: {field}")
            return False

    # Validate extractedIntelligence structure
    expected_intel_keys = [
        "bankAccounts",
        "upiIds",
        "phishingLinks",
        "phoneNumbers",
        "suspiciousKeywords"
    ]

    if "extractedIntelligence" in payload:
        for key in expected_intel_keys:
            if key not in payload["extractedIntelligence"]:
                logger.warning(f"⚠️ Missing intelligence field: {key}, adding empty array")
                payload["extractedIntelligence"][key] = []

    headers = {
        "Content-Type": "application/json"
    }

    logger.info("📦 Final Payload Ready for Callback")
    logger.info(f"📊 Intelligence Summary:")
    logger.info(f"   Bank Accounts: {len(payload.get('extractedIntelligence', {}).get('bankAccounts', []))}")
    logger.info(f"   UPI IDs: {len(payload.get('extractedIntelligence', {}).get('upiIds', []))}")
    logger.info(f"   Phishing Links: {len(payload.get('extractedIntelligence', {}).get('phishingLinks', []))}")
    logger.info(f"   Phone Numbers: {len(payload.get('extractedIntelligence', {}).get('phoneNumbers', []))}")
    logger.info(f"   Keywords: {len(payload.get('extractedIntelligence', {}).get('suspiciousKeywords', []))}")

    # -------------------------------
    # 2️⃣ Retry Logic (Exponential Backoff)
    # -------------------------------
    async with httpx.AsyncClient(timeout=10.0) as client:

        for attempt in range(3):
            try:
                logger.info(f"🚀 Sending callback to {url} (Attempt {attempt + 1})")

                response = await client.post(
                    url,
                    json=payload,
                    headers=headers
                )

                if response.status_code == 200:
                    logger.info("✅ Callback successful!")
                    logger.info(f"📥 Response: {response.text}")
                    return True

                logger.warning(
                    f"⚠️ Callback failed (Status {response.status_code}): {response.text}"
                )

            except httpx.TimeoutException:
                logger.error("⏳ Callback timeout")

            except httpx.RequestError as e:
                logger.error(f"🌐 Network error: {str(e)}")

            # Exponential backoff: 1s → 2s → 4s
            if attempt < 2:  # Don't wait after last attempt
                wait_time = 2 ** attempt
                logger.info(f"⏰ Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)

    logger.error("❌ Callback failed after 3 attempts.")
    return False
