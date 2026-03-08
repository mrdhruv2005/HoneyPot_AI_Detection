#!/usr/bin/env python3
"""
Export ALL accumulated intelligence data in GUVI JSON format
This aggregates data from ALL sessions to match dashboard totals
"""
import json
import redis

def get_all_intelligence():
    """Aggregate intelligence from all sessions"""
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    # Get all session keys
    session_keys = r.keys("session:*")
    
    # Aggregate all intelligence
    all_bank_accounts = []
    all_upi_ids = []
    all_phishing_links = []
    all_phone_numbers = []
    all_keywords = []
    total_messages = 0
    
    for key in session_keys:
        session_data = r.get(key)
        if session_data:
            session = json.loads(session_data)
            intel = session.get("intelligence", {})
            
            # Aggregate each type
            all_bank_accounts.extend(intel.get("bankAccounts", []))
            all_upi_ids.extend(intel.get("upiIds", []))
            all_phishing_links.extend(intel.get("phishingLinks", []))
            all_phone_numbers.extend(intel.get("phoneNumbers", []))
            all_keywords.extend(intel.get("suspiciousKeywords", []))
            
            total_messages += len(session.get("history", []))
    
    # Remove duplicates
    all_bank_accounts = list(set(all_bank_accounts))
    all_upi_ids = list(set(all_upi_ids))
    all_phishing_links = list(set(all_phishing_links))
    all_phone_numbers = list(set(all_phone_numbers))
    all_keywords = list(set(all_keywords))
    
    # Construct GUVI format with ALL accumulated data
    guvi_payload = {
        "sessionId": "aggregated-all-sessions",
        "scamDetected": True,
        "totalMessagesExchanged": total_messages,
        "extractedIntelligence": {
            "bankAccounts": all_bank_accounts,
            "upiIds": all_upi_ids,
            "phishingLinks": all_phishing_links,
            "phoneNumbers": all_phone_numbers,
            "suspiciousKeywords": all_keywords
        },
        "agentNotes": f"Aggregated intelligence from {len(session_keys)} sessions. Total entities: {len(all_bank_accounts) + len(all_upi_ids) + len(all_phishing_links) + len(all_phone_numbers)}"
    }
    
    return guvi_payload

if __name__ == "__main__":
    payload = get_all_intelligence()
    
    print("=" * 70)
    print("🎯 COMPLETE INTELLIGENCE DATA (ALL SESSIONS AGGREGATED)")
    print("=" * 70)
    print(json.dumps(payload, indent=2))
    print("\n" + "=" * 70)
    print(f"📊 TOTALS:")
    print(f"   Bank Accounts: {len(payload['extractedIntelligence']['bankAccounts'])}")
    print(f"   UPI IDs: {len(payload['extractedIntelligence']['upiIds'])}")
    print(f"   Phishing Links: {len(payload['extractedIntelligence']['phishingLinks'])}")
    print(f"   Phone Numbers: {len(payload['extractedIntelligence']['phoneNumbers'])}")
    print(f"   Suspicious Keywords: {len(payload['extractedIntelligence']['suspiciousKeywords'])}")
    print(f"   Total Messages: {payload['totalMessagesExchanged']}")
    print("=" * 70)
    
    # Save to file
    with open('aggregated_intelligence.json', 'w') as f:
        json.dump(payload, f, indent=2)
    
    print("✅ Saved to: aggregated_intelligence.json")
