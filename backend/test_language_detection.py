#!/usr/bin/env python3
"""
Test Language Detection and Response
"""
import asyncio
import sys
sys.path.insert(0, '/Users/jp710/Desktop/anti1/backend')

from services.agent_controller import AgentController

async def test_language_detection():
    print("=" * 80)
    print("🧪 TESTING LANGUAGE DETECTION & RESPONSE")
    print("=" * 80)
    
    agent = AgentController()
    
    # Test 1: English scammer
    print("\n" + "=" * 80)
    print("TEST 1: ENGLISH SCAMMER")
    print("=" * 80)
    
    english_msg = "Your account has been suspended! Click http://scam.com immediately"
    print(f"Scammer (English): {english_msg}")
    print(f"Detected Language: {agent.detect_language(english_msg)}")
    
    response = await agent.generate_response([], english_msg)
    print(f"Agent Response: {response}")
    
    # Test 2: Hindi scammer
    print("\n" + "=" * 80)
    print("TEST 2: HINDI SCAMMER")
    print("=" * 80)
    
    agent2 = AgentController()  # Fresh instance
    hindi_msg = "Aapka account suspend ho gaya hai. Abhi verify karo"
    print(f"Scammer (Hindi): {hindi_msg}")
    print(f"Detected Language: {agent2.detect_language(hindi_msg)}")
    
    response = await agent2.generate_response([], hindi_msg)
    print(f"Agent Response: {response}")
    
    # Test 3: Verify no typos or Hindi phrases in English response
    print("\n" + "=" * 80)
    print("TEST 3: VERIFY NO TYPOS OR HINDI PHRASES")
    print("=" * 80)
    
    agent3 = AgentController()
    test_msg = "Please verify your account"
    response = await agent3.generate_response([], test_msg)
    
    print(f"Response: {response}")
    
    # Check for unwanted patterns
    unwanted = ["okk", "yess", "wht", "pls", "thnks", "ji", "yaar", "bhai", "na?"]
    found_unwanted = [word for word in unwanted if word in response.lower()]
    
    if found_unwanted:
        print(f"❌ Found unwanted patterns: {found_unwanted}")
    else:
        print("✅ No typos or Hindi phrases found - Clean English response!")
    
    print("\n" + "=" * 80)
    print("✅ LANGUAGE DETECTION TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_language_detection())
