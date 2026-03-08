#!/usr/bin/env python3
"""
Test Complete Intelligence Callback Flow
"""
import asyncio
import sys
sys.path.insert(0, '/Users/jp710/Desktop/anti1/backend')

from services.callback import send_final_result

async def test_callback():
    print("=" * 80)
    print("🧪 TESTING COMPLETE INTELLIGENCE CALLBACK")
    print("=" * 80)
    
    # Simulated payload with all intelligence types
    test_payload = {
        "sessionId": "test-complete-intel",
        "scamDetected": True,
        "totalMessagesExchanged": 12,
        "extractedIntelligence": {
            "bankAccounts": ["1234567890123", "9876543210987"],
            "upiIds": ["scammer@paytm", "fraud@okaxis"],
            "phishingLinks": [
                "http://fake-bank.com/verify",
                "bit.ly/scam123",
                "www.phishing-site.com"
            ],
            "phoneNumbers": ["+919876543210", "9123456789"],
            "suspiciousKeywords": [
                "urgent",
                "verify now",
                "account blocked",
                "legal action",
                "download anydesk"
            ]
        },
        "agentNotes": "Complete intelligence test: ML=0.95, Rules=0.65. Risk=80%"
    }
    
    print("\n📦 Payload:")
    print(f"   Session: {test_payload['sessionId']}")
    print(f"   Scam Detected: {test_payload['scamDetected']}")
    print(f"   Messages: {test_payload['totalMessagesExchanged']}")
    print(f"\n📊 Intelligence:")
    for key, value in test_payload['extractedIntelligence'].items():
        print(f"   {key}: {len(value)} items")
        if value:
            print(f"      → {value[:2]}...")  # Show first 2 items
    
    print(f"\n{'='*80}")
    print("🚀 Sending to GUVI endpoint...")
    print(f"{'='*80}\n")
    
    success = await send_final_result(test_payload)
    
    print(f"\n{'='*80}")
    if success:
        print("✅ CALLBACK SUCCESSFUL!")
    else:
        print("❌ CALLBACK FAILED")
    print(f"{'='*80}")

if __name__ == "__main__":
    asyncio.run(test_callback())
