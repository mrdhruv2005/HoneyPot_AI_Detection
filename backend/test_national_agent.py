#!/usr/bin/env python3
"""
Test National-Level Agent Features
"""
import asyncio
import sys
sys.path.insert(0, '/Users/jp710/Desktop/anti1/backend')

from services.agent_controller import AgentController

async def test_national_level_features():
    print("=" * 80)
    print("🏆 TESTING NATIONAL-LEVEL AGENT FEATURES")
    print("=" * 80)
    
    agent = AgentController()
    history = []
    
    # Simulate realistic scam conversation
    scam_messages = [
        "Hello sir, this is from SBI Bank. Your account has been suspended due to suspicious activity.",
        "You need to verify your identity immediately or your account will be permanently blocked.",
        "Please download AnyDesk app and share the code with me so I can help you.",
        "This is very urgent sir. Police case will be filed if you don't act now.",
        "I am calling from Mumbai head office. My employee ID is SBI12345.",
        "You can verify by calling our official number +919876543210.",
        "For verification, please share your UPI ID and account number.",
        "We will refund Rs. 5000 to your account after verification.",
        "Please send payment to verify@paytm for processing.",
        "Visit our website http://sbi-verify.com for more details."
    ]
    
    for i, scam_msg in enumerate(scam_messages, 1):
        print(f"\n{'='*80}")
        print(f"🔴 Turn {i} - Scammer: {scam_msg}")
        print(f"{'='*80}")
        
        # Generate response
        response = await agent.generate_response(history, scam_msg)
        
        # Show agent state
        strategies = agent.get_strategy_blend()
        print(f"🟢 Agent: {response}")
        print(f"\n📊 Psychological State:")
        print(f"   Fear: {agent.fear:.1f}/5.0")
        print(f"   Confusion: {agent.confusion:.1f}/5.0")
        print(f"   Trust: {agent.trust:.1f}/5.0")
        print(f"   Suspicion: {agent.suspicion:.1f}/5.0")
        print(f"   Compliance: {agent.compliance_intent:.1f}/10.0")
        print(f"\n🎯 Active Strategies: {', '.join(strategies)}")
        print(f"🚩 Red Flags Detected: {agent.red_flags_detected}")
        
        # Update history
        history.append({"role": "user", "content": scam_msg})
        history.append({"role": "agent", "content": response})
        
        # Show intelligence if extracted
        if any(agent.intel.values()):
            print(f"\n🔍 Intelligence Collected:")
            for key, value in agent.intel.items():
                if value:
                    print(f"   {key}: {len(value)} items")
    
    print(f"\n{'='*80}")
    print("📋 FINAL INTELLIGENCE REPORT")
    print(f"{'='*80}")
    print(agent.export_intel())
    print(f"\n{'='*80}")
    print("✅ NATIONAL-LEVEL AGENT TEST COMPLETE")
    print(f"{'='*80}")

if __name__ == "__main__":
    asyncio.run(test_national_level_features())
