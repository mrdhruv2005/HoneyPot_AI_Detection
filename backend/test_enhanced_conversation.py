#!/usr/bin/env python3
"""
Test Enhanced Conversation System
"""
import asyncio
import sys
sys.path.insert(0, '/Users/jp710/Desktop/anti1/backend')

from services.agent_controller import AgentController

async def test_multi_turn_conversation():
    print("=" * 80)
    print("🧪 TESTING ENHANCED MULTI-TURN CONVERSATION")
    print("=" * 80)
    
    agent = AgentController()
    history = []
    
    # Simulate a multi-turn scam conversation
    scam_messages = [
        "Your bank account has been suspended due to suspicious activity!",
        "You need to verify your identity immediately or your account will be permanently blocked.",
        "Click this link to verify: http://fake-bank.com/verify",
        "You can also call our helpline at +919876543210",
        "We need your UPI ID to process the refund of Rs. 5000"
    ]
    
    for i, scam_msg in enumerate(scam_messages, 1):
        print(f"\n{'='*80}")
        print(f"🔴 Turn {i} - Scammer: {scam_msg}")
        print(f"{'='*80}")
        
        # Generate response
        response = await agent.generate_response(history, scam_msg)
        
        print(f"🟢 Agent (Strategy: {agent.strategy}): {response}")
        print(f"📊 Emotional State: Fear={agent.fear}/5, Confusion={agent.confusion}/5, Trust={agent.trust}/5")
        
        # Update history
        history.append({"role": "user", "content": scam_msg})
        history.append({"role": "agent", "content": response})
        
        # Show extracted intelligence
        if any(agent.extracted_intel.values()):
            print(f"🔍 Intel Extracted: {agent.extracted_intel}")
    
    print(f"\n{'='*80}")
    print("✅ MULTI-TURN CONVERSATION TEST COMPLETE")
    print(f"{'='*80}")
    print(f"Final Strategy: {agent.strategy}")
    print(f"Total Turns: {agent.turn_count}")
    print(f"Intelligence Gathered:")
    print(f"  - Links: {len(agent.extracted_intel['links'])}")
    print(f"  - Phone Numbers: {len(agent.extracted_intel['phone_numbers'])}")
    print(f"  - Payment Methods: {len(agent.extracted_intel['payment_methods'])}")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_multi_turn_conversation())
