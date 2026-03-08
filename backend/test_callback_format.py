#!/usr/bin/env python3
"""
Test script to show the exact GUVI callback JSON format
"""
import json
import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Get a session with intelligence
session_key = "session:public_guest:test-intel-session"
session_data = r.get(session_key)

if session_data:
    session = json.loads(session_data)
    
    # Construct GUVI callback payload (same as router.py)
    callback_payload = {
        "sessionId": "test-intel-session",
        "scamDetected": True,
        "totalMessagesExchanged": len(session.get("history", [])),
        "extractedIntelligence": session.get("intelligence", {}),
        "agentNotes": "Detected scam logic: ML=0.85, Rules=0.70."
    }
    
    print("=" * 60)
    print("GUVI CALLBACK PAYLOAD (JSON FORMAT)")
    print("=" * 60)
    print(json.dumps(callback_payload, indent=2))
    print("\n" + "=" * 60)
    print("✅ This is the exact format sent to GUVI endpoint")
    print("=" * 60)
else:
    print("❌ Session not found. Send a scam message first!")
