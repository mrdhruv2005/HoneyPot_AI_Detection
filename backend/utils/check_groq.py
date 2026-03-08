import asyncio
import os
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()

async def main():
    api_key = os.getenv("GROQ_API_KEY")
    print(f"Testing API Key: {api_key[:10]}...")
    
    try:
        client = AsyncGroq(api_key=api_key)
        chat_completion = await client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Explain what a honeypot is in 10 words.",
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        print("SUCCESS:", chat_completion.choices[0].message.content)
    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":
    asyncio.run(main())
