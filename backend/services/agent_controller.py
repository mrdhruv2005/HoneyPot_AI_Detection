from core.config import get_settings
from groq import AsyncGroq
import random
import logging
import re
import json
from datetime import datetime
from collections import deque

settings = get_settings()
logger = logging.getLogger("scam_intel_agent")


class AgentController:
    """
    National-Level Scam Honeypot Agent
    Features:
    - Behavioral memory consistency
    - Adaptive suspicion modeling
    - Delayed compliance simulation
    - Controlled mistake injection
    - Structured intelligence harvesting
    - Non-repetitive linguistic variation
    - Micro-strategy blending
    """

    def __init__(self):
        self.client = None
        if settings.GROQ_API_KEY:
            try:
                self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
                logger.info("Groq Async Client Initialized")
            except Exception as e:
                logger.error(f"Groq init failed: {e}")

        # ============ Behavioral Memory System ============
        self.turn_count = 0
        self.conversation_memory = deque(maxlen=20)  # Remember last 20 exchanges
        self.mentioned_facts = set()  # Track what victim has said
        self.scammer_claims = []  # Track scammer's claims for consistency checking
        
        # ============ Psychological State (Dynamic) ============
        self.fear = 1.0
        self.confusion = 2.0
        self.trust = 1.0
        self.suspicion = 2.0
        self.compliance_intent = 1.0
        self.urgency_perception = 1.0
        
        # ============ Adaptive Suspicion Modeling ============
        self.red_flags_detected = 0
        self.trust_decay_rate = 0.1
        self.last_question_type = None
        
        # ============ Delayed Compliance Simulation ============
        self.compliance_threshold = 7.0  # Needs to reach this to "comply"
        self.hesitation_count = 0
        self.family_mention_count = 0
        
        # ============ Controlled Mistake Injection ============
        self.mistake_probability = 0.15
        self.last_mistake_turn = 0
        
        # ============ Intelligence Harvesting ============
        self.intel = {
            "links": [],
            "phone_numbers": [],
            "upi_ids": [],
            "bank_accounts": [],
            "names": [],
            "organizations": [],
            "locations": [],
            "keywords": []
        }
        
        # ============ Linguistic Variation System ============
        self.response_templates = {
            "confusion": [
                "I don't understand what you mean...",
                "Can you explain that more clearly?",
                "Wait, what exactly are you saying?",
                "I'm confused about this...",
                "This doesn't make sense to me..."
            ],
            "fear": [
                "Oh no, is this serious?",
                "Am I in trouble?",
                "What will happen if I don't do this?",
                "This sounds really bad...",
                "Should I be worried?"
            ],
            "hesitation": [
                "I'm not sure about this...",
                "Can I think about it first?",
                "Should I check with someone?",
                "Is this really necessary?",
                "I need to verify this..."
            ],
            "compliance_building": [
                "Okay, what do I need to do?",
                "How can I fix this?",
                "What's the next step?",
                "Tell me what to do...",
                "I want to resolve this..."
            ],
            "information_extraction": [
                "What's your name again?",
                "Which company did you say you're from?",
                "Can you give me your employee ID?",
                "What's your contact number?",
                "Where is your office located?"
            ]
        }

    # ========================================================
    # 🧠 Behavioral Memory & Consistency
    # ========================================================

    def remember_fact(self, fact):
        """Store facts the victim has mentioned for consistency"""
        self.mentioned_facts.add(fact.lower())
    
    def check_consistency(self, new_statement):
        """Ensure victim doesn't contradict previous statements"""
        # Simple check - can be expanded
        return new_statement.lower() not in self.mentioned_facts

    # ========================================================
    # 🎯 Adaptive Suspicion Modeling
    # ========================================================

    def update_suspicion(self, scammer_msg):
        """Dynamically adjust suspicion based on red flags"""
        msg = scammer_msg.lower()
        
        # Red flag detection
        red_flags = [
            ("gift card", 2.0),
            ("bitcoin", 2.5),
            ("urgent", 0.5),
            ("immediately", 0.5),
            ("police", 1.0),
            ("arrest", 1.5),
            ("legal action", 1.5),
            ("suspended", 0.8),
            ("blocked", 0.8),
            ("verify now", 0.7),
            ("click here", 1.0),
            ("download", 1.2),
            ("remote access", 2.0),
            ("anydesk", 2.0),
            ("teamviewer", 2.0)
        ]
        
        for flag, weight in red_flags:
            if flag in msg:
                self.suspicion += weight
                self.red_flags_detected += 1
                logger.info(f"Red flag detected: {flag} (+{weight} suspicion)")
        
        # Trust decay over time if too many red flags
        if self.red_flags_detected > 3:
            self.trust = max(1.0, self.trust - self.trust_decay_rate)

    # ========================================================
    # 📊 Psychological State Evolution
    # ========================================================

    def update_psychology(self, scammer_msg):
        """Advanced psychological state modeling"""
        self.turn_count += 1
        msg = scammer_msg.lower()
        
        # Fear dynamics
        if any(word in msg for word in ["urgent", "immediately", "now", "quick"]):
            self.fear += 0.5
            self.urgency_perception += 0.8
        
        if any(word in msg for word in ["police", "legal", "arrest", "court"]):
            self.fear += 1.5
            self.urgency_perception += 1.2
        
        # Confusion dynamics
        if any(word in msg for word in ["click", "download", "install", "remote"]):
            self.confusion += 0.8
        
        # Trust dynamics (builds slowly with "official" language)
        if any(word in msg for word in ["official", "bank", "government", "authorized"]):
            self.trust += 0.3
        else:
            self.trust = max(1.0, self.trust - 0.1)  # Slow decay
        
        # Compliance intent (gradual build-up)
        if self.turn_count > 5:
            self.compliance_intent += 0.2
        
        if self.fear > 3.0:
            self.compliance_intent += 0.5
        
        # Cap all values
        self.fear = min(self.fear, 5.0)
        self.confusion = min(self.confusion, 5.0)
        self.trust = min(self.trust, 5.0)
        self.suspicion = min(self.suspicion, 5.0)
        self.compliance_intent = min(self.compliance_intent, 10.0)
        self.urgency_perception = min(self.urgency_perception, 5.0)
        
        # Update suspicion model
        self.update_suspicion(scammer_msg)

    # ========================================================
    # 🔍 Structured Intelligence Harvesting
    # ========================================================

    def extract_intel(self, text):
        """Advanced pattern-based intelligence extraction"""
        # URLs
        urls = re.findall(r'https?://\S+|www\.\S+|\S+\.com\S*', text)
        self.intel["links"].extend(urls)
        
        # Phone numbers (Indian and international)
        phones = re.findall(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        self.intel["phone_numbers"].extend(phones)
        
        # UPI IDs
        upi_ids = re.findall(r'[\w.-]+@[\w]+', text)
        self.intel["upi_ids"].extend(upi_ids)
        
        # Bank account numbers (9-18 digits)
        bank_accounts = re.findall(r'\b\d{9,18}\b', text)
        self.intel["bank_accounts"].extend(bank_accounts)
        
        # Names (capitalized words, 2-3 words)
        names = re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+(?:\s[A-Z][a-z]+)?\b', text)
        self.intel["names"].extend(names)
        
        # Organizations/Banks
        org_keywords = ["bank", "sbi", "hdfc", "icici", "axis", "paytm", "phonepe", "gpay", "government"]
        for keyword in org_keywords:
            if keyword in text.lower():
                self.intel["organizations"].append(keyword)
        
        # Log extraction
        if any([urls, phones, upi_ids, bank_accounts, names]):
            logger.info(f"Intel extracted: URLs={len(urls)}, Phones={len(phones)}, UPIs={len(upi_ids)}, Banks={len(bank_accounts)}, Names={len(names)}")

    # ========================================================
    # 🎭 Controlled Mistake Injection
    # ========================================================

    def inject_human_mistakes(self, text):
        """Add realistic human mistakes"""
        if self.turn_count - self.last_mistake_turn < 3:
            return text  # Don't make mistakes too frequently
        
        if random.random() < self.mistake_probability:
            self.last_mistake_turn = self.turn_count
            
            mistake_type = random.choice(["typo", "pause", "repetition", "incomplete"])
            
            if mistake_type == "typo":
                # Common typos
                typos = {
                    "the": "teh",
                    "you": "yu",
                    "what": "wht",
                    "okay": "okk",
                    "yes": "yess"
                }
                for correct, typo in typos.items():
                    if correct in text.lower():
                        text = text.replace(correct, typo, 1)
                        break
            
            elif mistake_type == "pause":
                # Add ellipsis for thinking
                if not text.endswith("..."):
                    text += "..."
            
            elif mistake_type == "repetition":
                # Repeat first word
                words = text.split()
                if len(words) > 2:
                    text = f"{words[0]} {words[0]} {' '.join(words[1:])}"
            
            elif mistake_type == "incomplete":
                # Cut off sentence
                if len(text) > 20:
                    text = text[:len(text)//2] + "... wait"
        
        return text

    # ========================================================
    # 🎨 Non-Repetitive Linguistic Variation
    # ========================================================

    def get_varied_response(self, category):
        """Get a response template and remove it to avoid repetition"""
        if category in self.response_templates and self.response_templates[category]:
            response = random.choice(self.response_templates[category])
            # Remove used response to avoid repetition
            self.response_templates[category].remove(response)
            # Replenish if empty
            if not self.response_templates[category]:
                self.replenish_templates(category)
            return response
        return "I'm not sure what to say..."
    
    def replenish_templates(self, category):
        """Replenish response templates"""
        templates = {
            "confusion": [
                "I don't understand what you mean...",
                "Can you explain that more clearly?",
                "Wait, what exactly are you saying?",
                "I'm confused about this...",
                "This doesn't make sense to me..."
            ],
            "fear": [
                "Oh no, is this serious?",
                "Am I in trouble?",
                "What will happen if I don't do this?",
                "This sounds really bad...",
                "Should I be worried?"
            ],
            "hesitation": [
                "I'm not sure about this...",
                "Can I think about it first?",
                "Should I check with someone?",
                "Is this really necessary?",
                "I need to verify this..."
            ],
            "compliance_building": [
                "Okay, what do I need to do?",
                "How can I fix this?",
                "What's the next step?",
                "Tell me what to do...",
                "I want to resolve this..."
            ],
            "information_extraction": [
                "What's your name again?",
                "Which company did you say you're from?",
                "Can you give me your employee ID?",
                "What's your contact number?",
                "Where is your office located?"
            ]
        }
        if category in templates:
            self.response_templates[category] = templates[category].copy()

    # ========================================================
    # 🧩 Micro-Strategy Blending
    # ========================================================

    def get_strategy_blend(self):
        """Calculate micro-strategy weights based on psychological state"""
        # Not rigid stages - fluid blending based on state
        
        confusion_weight = self.confusion / 5.0
        fear_weight = self.fear / 5.0
        trust_weight = self.trust / 5.0
        compliance_weight = self.compliance_intent / 10.0
        
        # Determine dominant micro-strategies
        strategies = []
        
        if confusion_weight > 0.4:
            strategies.append("ask_clarification")
        
        if fear_weight > 0.5:
            strategies.append("express_worry")
        
        if trust_weight < 0.3 or self.suspicion > 3.0:
            strategies.append("request_verification")
        
        if compliance_weight > 0.5:
            strategies.append("show_willingness")
        
        if self.turn_count > 5 and compliance_weight > 0.6:
            strategies.append("extract_information")
        
        if not strategies:
            strategies.append("neutral_inquiry")
        
        return strategies

    # ========================================================
    # 🏗️ Dynamic Prompt Construction
    # ========================================================

    def build_dynamic_prompt(self, scammer_msg):
        """Build context-aware prompt based on current state"""
        
        strategies = self.get_strategy_blend()
        
        psychological_state = f"""
Current Psychological State:
- Fear: {self.fear:.1f}/5.0 {"(HIGH)" if self.fear > 3.5 else ""}
- Confusion: {self.confusion:.1f}/5.0
- Trust: {self.trust:.1f}/5.0
- Suspicion: {self.suspicion:.1f}/5.0 {"(ALERT)" if self.suspicion > 3.5 else ""}
- Compliance Intent: {self.compliance_intent:.1f}/10.0
- Urgency Perception: {self.urgency_perception:.1f}/5.0
- Turn: {self.turn_count}
- Red Flags Detected: {self.red_flags_detected}
"""

        active_strategies = f"""
Active Micro-Strategies: {', '.join(strategies)}
"""

        behavioral_guidelines = """
You are a normal Indian adult who received a suspicious message.

CORE BEHAVIOR:
- You are concerned but not tech-savvy
- You ask basic questions to understand
- You show hesitation before complying
- You occasionally mention checking with family/friends
- You are NOT immediately compliant
- You sound natural and human

CRITICAL RULES:
1. NEVER reveal you know it's a scam
2. NEVER say you're AI or a bot
3. Keep responses SHORT (1-3 sentences)
4. Sound natural and conversational
5. Ask questions that extract information
6. Show appropriate emotions based on your state
7. Be consistent with what you've said before
8. Occasionally hesitate or make small mistakes
"""

        intelligence_extraction_bias = ""
        if "extract_information" in strategies:
            intelligence_extraction_bias = """
INTELLIGENCE EXTRACTION MODE:
Subtly ask for:
- Their full name and employee ID
- Company/bank name and branch
- Official contact number
- UPI ID or payment details
- Official website or verification link
- Physical office address

Frame it as "I need to verify this is real" or "For my records"
"""

        return f"""{behavioral_guidelines}

{psychological_state}

{active_strategies}

{intelligence_extraction_bias}

Return the response in the SAME LANGUAGE as the scammer's message.
- If they speak English -> Respond in English ONLY.
- If they speak Hindi -> Respond in Hindi (or Hinglish) ONLY.
- If they mix languages -> You can mix them too.

Scammer just said:
"{scammer_msg}"

Respond naturally as a real person would.
"""

    # ========================================================
    # 🛡️ Safety & Validation
    # ========================================================

    def validate(self, response):
        """Prevent AI leakage"""
        forbidden_patterns = [
            r'\bAI\b', r'\bbot\b', r'\blanguage model\b',
            r'\bscam\b', r'\bfraud\b', r'\bhoneypot\b'
        ]
        
        for pattern in forbidden_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                logger.warning(f"AI leakage detected: {pattern}")
                return self.get_varied_response("confusion")
        
        if len(response.split()) > 60:
            return "Sorry, I'm confused... what exactly should I do?"
        
        return response.strip()

    # ========================================================
    # 🤖 Main Generation Engine
    # ========================================================

    async def generate_response(self, history: list, scammer_msg: str):
        """Generate intelligent, adaptive response"""
        
        if not self.client:
            return self.get_varied_response("confusion")
        
        # Update all systems
        self.update_psychology(scammer_msg)
        self.extract_intel(scammer_msg)
        self.conversation_memory.append({"role": "scammer", "msg": scammer_msg})
        
        # Build dynamic prompt
        system_prompt = self.build_dynamic_prompt(scammer_msg)
        
        try:
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history
            for msg in history[-8:]:
                role = "assistant" if msg.get("role") == "agent" else "user"
                messages.append({
                    "role": role,
                    "content": msg.get("content", "")
                })
            
            messages.append({"role": "user", "content": scammer_msg})
            
            # Generate response
            chat_completion = await self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.95,  # High variation
                max_tokens=150
            )
            
            reply = chat_completion.choices[0].message.content
            
            # Post-processing
            reply = self.validate(reply)
            reply = self.inject_human_mistakes(reply)
            
            # Store in memory
            self.conversation_memory.append({"role": "agent", "msg": reply})
            
            logger.info(f"Turn {self.turn_count}: Strategies={self.get_strategy_blend()}, Fear={self.fear:.1f}, Suspicion={self.suspicion:.1f}")
            
            return reply
        
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return self.get_varied_response("confusion")

    # ========================================================
    # 🌊 Streaming Response (for SSE endpoint)
    # ========================================================

    async def generate_response_stream(self, history: list, scammer_msg: str):
        """Streaming version for real-time chat"""
        
        if not self.client:
            yield self.get_varied_response("confusion")
            return
        
        # Update all systems
        self.update_psychology(scammer_msg)
        self.extract_intel(scammer_msg)
        self.conversation_memory.append({"role": "scammer", "msg": scammer_msg})
        
        # Build dynamic prompt
        system_prompt = self.build_dynamic_prompt(scammer_msg)
        
        try:
            messages = [{"role": "system", "content": system_prompt}]
            
            for msg in history[-8:]:
                role = "assistant" if msg.get("role") == "agent" else "user"
                messages.append({
                    "role": role,
                    "content": msg.get("content", "")
                })
            
            messages.append({"role": "user", "content": scammer_msg})
            
            logger.info(f"Stream Turn {self.turn_count}: Strategies={self.get_strategy_blend()}")
            
            stream = await self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.95,
                max_tokens=150,
                stream=True
            )
            
            full_response = ""
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    yield content
            
            # Post-process full response
            full_response = self.validate(full_response)
            self.conversation_memory.append({"role": "agent", "msg": full_response})
            
            logger.info(f"Stream complete: Fear={self.fear:.1f}, Suspicion={self.suspicion:.1f}, Intel={len(self.intel['links'])} links")
        
        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield self.get_varied_response("confusion")

    # ========================================================
    # 📊 Intelligence Export
    # ========================================================

    def export_intel(self):
        """Export all collected intelligence"""
        return json.dumps({
            "intelligence": self.intel,
            "statistics": {
                "turns": self.turn_count,
                "red_flags": self.red_flags_detected,
                "final_suspicion": round(self.suspicion, 2),
                "final_trust": round(self.trust, 2)
            },
            "conversation_summary": list(self.conversation_memory)
        }, indent=2)
