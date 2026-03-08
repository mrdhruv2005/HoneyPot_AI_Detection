#!/usr/bin/env python3
"""
Test Scam Detection with Different Messages
"""
import sys
sys.path.insert(0, '/Users/jp710/Desktop/anti1/backend')

from services.ml_engine import MLEngine
from services.rule_engine import RuleEngine

def test_detection():
    ml = MLEngine()
    rule = RuleEngine()
    
    test_messages = [
        "Your bank account has been suspended. Verify immediately.",
        "Hello, how are you?",
        "Click this link to verify: http://scam.com",
        "Download AnyDesk now",
        "Pay Rs. 5000 via gift card",
        "Meeting at 3 PM",
        "Police case filed. Pay fine now.",
        "Your order is shipped"
    ]
    
    print("=" * 80)
    print("🧪 SCAM DETECTION THRESHOLD TEST")
    print("=" * 80)
    print(f"Threshold: 40% (was 60%)")
    print("=" * 80)
    
    for msg in test_messages:
        ml_score = ml.predict(msg)
        rule_score = rule.analyze(msg)
        risk = (0.5 * ml_score) + (0.5 * rule_score)
        detected = risk > 0.4
        
        print(f"\nMessage: {msg[:50]}...")
        print(f"  ML: {ml_score:.1%} | Rule: {rule_score:.1%} | Combined: {risk:.1%}")
        print(f"  {'✅ SCAM DETECTED' if detected else '❌ Safe'}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    test_detection()
