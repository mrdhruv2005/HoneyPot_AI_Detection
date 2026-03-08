#!/usr/bin/env python3
"""
Test the updated Sam persona agent
"""
import asyncio
import sys
sys.path.insert(0, '/Users/jp710/Desktop/anti1/backend')

from services.agent_controller import AgentController

async def test_agent():
    print("=" * 80)
    print("🧪 TESTING UPDATED SAM PERSONA")
    print("=" * 80)
    
    agent = AgentController()
    
    # Simulated conversation history
    history = [
        {"role": "user", "content": "Your account has been suspended due to suspicious activity."},
        {"role": "agent", "content": "What? My account is suspended? What happened?"},
    ]
    
    # Test message from scammer
    scam_message = "You need to verify your identity immediately. Click this link: http://bit.ly/verify123 or call us at +919876543210"
    
    print(f"\n📨 Scammer: {scam_message}")
    print(f"\n🤖 Sam is typing...\n")
    
    # Test response generation
    response = await agent.generate_response(history, scam_message)
    
    print(f"💬 Sam: {response}")
    print(f"\n📊 Extracted Intel: {agent.extracted_intel}")
    
    print("\n" + "=" * 80)
    print("✅ Agent Controller Test Complete!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_agent())
