#!/usr/bin/env python3
"""
Test Enhanced ML and Rule Engine
"""
import sys
sys.path.insert(0, '/Users/jp710/Desktop/anti1/backend')

from services.ml_engine import MLEngine
from services.rule_engine import RuleEngine

def test_scam_detection():
    print("=" * 80)
    print("🧪 TESTING ENHANCED SCAM DETECTION ENGINES")
    print("=" * 80)
    
    # Initialize engines
    ml_engine = MLEngine()
    rule_engine = RuleEngine()
    
    # Test messages
    test_cases = [
        {
            "text": "Your bank account has been suspended. Verify immediately or face legal action.",
            "expected": "scam"
        },
        {
            "text": "Download AnyDesk and share code. Your account will be blocked.",
            "expected": "scam"
        },
        {
            "text": "Congratulations! You won Rs. 25 lakhs. Pay processing fee via gift card.",
            "expected": "scam"
        },
        {
            "text": "Police case filed. Pay fine immediately to avoid arrest.",
            "expected": "scam"
        },
        {
            "text": "Your OTP for login is 123456. Valid for 10 minutes.",
            "expected": "legitimate"
        },
        {
            "text": "Meeting scheduled for 3 PM today. Please confirm.",
            "expected": "legitimate"
        },
        {
            "text": "Your order has been shipped and will arrive tomorrow.",
            "expected": "legitimate"
        }
    ]
    
    print("\n📊 TESTING SCAM DETECTION\n")
    
    correct_ml = 0
    correct_rule = 0
    
    for i, case in enumerate(test_cases, 1):
        text = case["text"]
        expected = case["expected"]
        
        print(f"\n{'='*80}")
        print(f"Test {i}: {text[:60]}...")
        print(f"Expected: {expected.upper()}")
        print(f"{'='*80}")
        
        # ML Engine prediction
        ml_result = ml_engine.predict_with_confidence(text)
        ml_prediction = "scam" if ml_result["is_scam"] else "legitimate"
        ml_prob = ml_result["probability"]
        
        print(f"\n🤖 ML Engine:")
        print(f"   Prediction: {ml_prediction.upper()}")
        print(f"   Scam Probability: {ml_prob:.2%}")
        print(f"   Confidence: {ml_result['confidence'].upper()}")
        
        if ml_prediction == expected:
            print(f"   ✅ CORRECT")
            correct_ml += 1
        else:
            print(f"   ❌ INCORRECT")
        
        # Rule Engine analysis
        rule_score = rule_engine.analyze(text)
        rule_prediction = "scam" if rule_score >= 0.5 else "legitimate"
        detailed = rule_engine.get_detailed_analysis(text)
        
        print(f"\n📋 Rule Engine:")
        print(f"   Prediction: {rule_prediction.upper()}")
        print(f"   Scam Score: {rule_score:.2%}")
        print(f"   Risk Level: {detailed['risk_level'].upper()}")
        print(f"   Categories: {', '.join(detailed['categories_detected'])}")
        if detailed['red_flags']:
            print(f"   Red Flags: {', '.join(detailed['red_flags'][:2])}")
        
        if rule_prediction == expected:
            print(f"   ✅ CORRECT")
            correct_rule += 1
        else:
            print(f"   ❌ INCORRECT")
    
    print(f"\n{'='*80}")
    print("📈 FINAL RESULTS")
    print(f"{'='*80}")
    print(f"ML Engine Accuracy: {correct_ml}/{len(test_cases)} ({correct_ml/len(test_cases)*100:.1f}%)")
    print(f"Rule Engine Accuracy: {correct_rule}/{len(test_cases)} ({correct_rule/len(test_cases)*100:.1f}%)")
    print(f"{'='*80}")
    
    # Test keyword coverage
    print(f"\n{'='*80}")
    print("📚 KEYWORD COVERAGE")
    print(f"{'='*80}")
    print(f"Urgency keywords: {len(rule_engine.urgency_keywords)}")
    print(f"Threat keywords: {len(rule_engine.threat_keywords)}")
    print(f"Legal keywords: {len(rule_engine.legal_keywords)}")
    print(f"Financial lure keywords: {len(rule_engine.financial_lure_keywords)}")
    print(f"Payment keywords: {len(rule_engine.payment_keywords)}")
    print(f"Tech support keywords: {len(rule_engine.tech_support_keywords)}")
    print(f"Info request keywords: {len(rule_engine.info_request_keywords)}")
    print(f"Impersonation keywords: {len(rule_engine.impersonation_keywords)}")
    print(f"Phishing indicators: {len(rule_engine.phishing_indicators)}")
    print(f"Indian scam keywords: {len(rule_engine.indian_scam_keywords)}")
    
    total_keywords = (
        len(rule_engine.urgency_keywords) +
        len(rule_engine.threat_keywords) +
        len(rule_engine.legal_keywords) +
        len(rule_engine.financial_lure_keywords) +
        len(rule_engine.payment_keywords) +
        len(rule_engine.tech_support_keywords) +
        len(rule_engine.info_request_keywords) +
        len(rule_engine.impersonation_keywords) +
        len(rule_engine.phishing_indicators) +
        len(rule_engine.indian_scam_keywords)
    )
    
    print(f"\n🎯 TOTAL SCAM KEYWORDS: {total_keywords}")
    print(f"{'='*80}")

if __name__ == "__main__":
    test_scam_detection()
