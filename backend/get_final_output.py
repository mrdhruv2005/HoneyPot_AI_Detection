#!/usr/bin/env python3
"""
Export FINAL INTELLIGENCE DATA matching dashboard totals
This shows the EXACT data that matches what you see on the dashboard
"""
import json
import redis

def get_dashboard_intelligence():
    """Get intelligence data matching dashboard display"""
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    # Get dashboard stats (these are the counts shown on dashboard)
    bank_accounts_count = int(r.get("stats:public_guest:bank_accounts_extracted") or 0)
    upi_ids_count = int(r.get("stats:public_guest:upi_ids_extracted") or 0)
    phishing_links_count = int(r.get("stats:public_guest:phishing_links_extracted") or 0)
    phone_numbers_count = int(r.get("stats:public_guest:phone_numbers_extracted") or 0)
    total_messages = int(r.get("stats:public_guest:total_messages") or 0)
    scams_detected = int(r.get("stats:public_guest:scams_detected") or 0)
    
    # Get actual unique intelligence data from all sessions
    session_keys = r.keys("session:*")
    
    all_bank_accounts = []
    all_upi_ids = []
    all_phishing_links = []
    all_phone_numbers = []
    all_keywords = []
    
    for key in session_keys:
        session_data = r.get(key)
        if session_data:
            session = json.loads(session_data)
            intel = session.get("intelligence", {})
            
            all_bank_accounts.extend(intel.get("bankAccounts", []))
            all_upi_ids.extend(intel.get("upiIds", []))
            all_phishing_links.extend(intel.get("phishingLinks", []))
            all_phone_numbers.extend(intel.get("phoneNumbers", []))
            all_keywords.extend(intel.get("suspiciousKeywords", []))
    
    # Remove duplicates for unique values
    unique_bank_accounts = list(set(all_bank_accounts))
    unique_upi_ids = list(set(all_upi_ids))
    unique_phishing_links = list(set(all_phishing_links))
    unique_phone_numbers = list(set(all_phone_numbers))
    unique_keywords = list(set(all_keywords))
    
    # FINAL GUVI PAYLOAD
    final_payload = {
        "sessionId": "aggregated-all-sessions",
        "scamDetected": scams_detected > 0,
        "totalMessagesExchanged": total_messages,
        "extractedIntelligence": {
            "bankAccounts": unique_bank_accounts,
            "upiIds": unique_upi_ids,
            "phishingLinks": unique_phishing_links,
            "phoneNumbers": unique_phone_numbers,
            "suspiciousKeywords": unique_keywords
        },
        "agentNotes": f"Total extractions: {bank_accounts_count} bank accounts, {upi_ids_count} UPI IDs, {phishing_links_count} phishing links, {phone_numbers_count} phone numbers across {len(session_keys)} sessions",
        "dashboardStats": {
            "totalBankAccountsExtracted": bank_accounts_count,
            "totalUpiIdsExtracted": upi_ids_count,
            "totalPhishingLinksExtracted": phishing_links_count,
            "totalPhoneNumbersExtracted": phone_numbers_count,
            "totalMessages": total_messages,
            "scamsDetected": scams_detected
        }
    }
    
    return final_payload

if __name__ == "__main__":
    payload = get_dashboard_intelligence()
    
    print("=" * 80)
    print("🎯 FINAL INTELLIGENCE OUTPUT (MATCHES DASHBOARD)")
    print("=" * 80)
    print(json.dumps(payload, indent=2))
    print("\n" + "=" * 80)
    print("📊 DASHBOARD TOTALS (Total Extractions Including Duplicates):")
    print(f"   ✅ Bank Accounts: {payload['dashboardStats']['totalBankAccountsExtracted']}")
    print(f"   ✅ UPI IDs: {payload['dashboardStats']['totalUpiIdsExtracted']}")
    print(f"   ✅ Phishing Links: {payload['dashboardStats']['totalPhishingLinksExtracted']}")
    print(f"   ✅ Phone Numbers: {payload['dashboardStats']['totalPhoneNumbersExtracted']}")
    print(f"   ✅ Total Messages: {payload['dashboardStats']['totalMessages']}")
    print(f"   ✅ Scams Detected: {payload['dashboardStats']['scamsDetected']}")
    print("\n📋 UNIQUE VALUES (Actual Extracted Data):")
    print(f"   • Unique Bank Accounts: {len(payload['extractedIntelligence']['bankAccounts'])}")
    print(f"   • Unique UPI IDs: {len(payload['extractedIntelligence']['upiIds'])}")
    print(f"   • Unique Phishing Links: {len(payload['extractedIntelligence']['phishingLinks'])}")
    print(f"   • Unique Phone Numbers: {len(payload['extractedIntelligence']['phoneNumbers'])}")
    print("=" * 80)
    
    # Save to file
    with open('final_intelligence_output.json', 'w') as f:
        json.dump(payload, f, indent=2)
    
    print("\n✅ Saved to: final_intelligence_output.json")
    print("📍 Location: /Users/jp710/Desktop/anti1/backend/final_intelligence_output.json")
