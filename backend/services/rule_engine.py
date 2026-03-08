import re
import logging

logger = logging.getLogger("rule_engine")

class RuleEngine:
    """
    Enhanced Rule-Based Scam Detection Engine
    Features:
    - 100+ scam keywords across 10 categories
    - Advanced pattern matching
    - Weighted scoring system
    - Indian scam pattern detection
    """
    
    def __init__(self):
        # ============ Comprehensive Scam Keywords ============
        
        # Category 1: Urgency & Pressure Tactics
        self.urgency_keywords = [
            r"immediately", r"urgent", r"asap", r"right now", r"hurry",
            r"expires? (?:in|today|soon)", r"limited time", r"act now",
            r"don't wait", r"time sensitive", r"last chance", r"final notice",
            r"within \d+ (?:hours?|minutes?|days?)", r"before (?:midnight|today)",
            r"quick(?:ly)?", r"instant", r"fast", r"rush"
        ]
        
        # Category 2: Account/Security Threats
        self.threat_keywords = [
            r"blocked", r"suspended", r"locked", r"frozen", r"disabled",
            r"deactivated", r"closed", r"terminated", r"restricted",
            r"unauthorized (?:access|activity|transaction)",
            r"suspicious activity", r"security (?:alert|breach|issue)",
            r"compromised", r"hacked", r"fraud(?:ulent)?",
            r"unusual activity", r"verify (?:your )?(?:account|identity)",
            r"confirm (?:your )?(?:account|identity|details)",
            r"update (?:your )?(?:account|information|details)"
        ]
        
        # Category 3: Legal/Authority Threats
        self.legal_keywords = [
            r"police", r"legal action", r"court", r"lawsuit", r"arrest",
            r"warrant", r"investigation", r"criminal", r"penalty",
            r"fine", r"jail", r"prison", r"prosecution", r"charges?",
            r"government", r"tax department", r"income tax", r"gst",
            r"enforcement", r"cyber crime", r"fir", r"case filed"
        ]
        
        # Category 4: Financial Lures
        self.financial_lure_keywords = [
            r"won", r"winner", r"prize", r"lottery", r"jackpot",
            r"refund", r"cashback", r"reward", r"bonus", r"gift",
            r"free (?:money|cash|gift)", r"claim (?:your )?(?:prize|reward)",
            r"congratulations", r"selected", r"lucky",
            r"compensation", r"settlement", r"inheritance",
            r"investment opportunity", r"guaranteed (?:returns?|profit)",
            r"double your money", r"earn (?:lakhs?|crores?)",
            r"work from home", r"part[- ]?time job"
        ]
        
        # Category 5: Payment/Money Requests
        self.payment_keywords = [
            r"send (?:money|payment|amount)", r"transfer (?:money|funds)",
            r"pay (?:now|immediately)", r"deposit", r"wire transfer",
            r"western union", r"moneygram", r"gift card",
            r"google play", r"amazon card", r"itunes card",
            r"bitcoin", r"cryptocurrency", r"crypto", r"usdt", r"btc",
            r"paytm", r"phonepe", r"gpay", r"upi",
            r"processing fee", r"handling (?:fee|charge)",
            r"advance payment", r"upfront (?:fee|payment)"
        ]
        
        # Category 6: Remote Access/Tech Support
        self.tech_support_keywords = [
            r"anydesk", r"teamviewer", r"remote (?:access|desktop|support)",
            r"download (?:this )?(?:app|software|tool)",
            r"install", r"screen share", r"share (?:your )?screen",
            r"tech(?:nical)? support", r"customer (?:care|support)",
            r"helpdesk", r"it (?:support|team)", r"virus detected",
            r"malware", r"computer (?:error|problem)", r"windows support"
        ]
        
        # Category 7: Personal Information Requests
        self.info_request_keywords = [
            r"(?:share|provide|send|give) (?:your )?(?:otp|password|pin)",
            r"(?:share|provide|send|give) (?:your )?(?:cvv|card number)",
            r"(?:share|provide|send|give) (?:your )?(?:account|bank) (?:number|details)",
            r"(?:share|provide|send|give) (?:your )?(?:aadhaar|pan|passport)",
            r"(?:share|provide|send|give) (?:your )?(?:personal|confidential) (?:information|details)",
            r"verify (?:your )?(?:otp|code|pin)",
            r"enter (?:your )?(?:otp|password|pin|cvv)",
            r"social security", r"date of birth", r"mother'?s maiden name"
        ]
        
        # Category 8: Impersonation Indicators
        self.impersonation_keywords = [
            r"(?:i am|this is) (?:from|calling from)",
            r"(?:sbi|hdfc|icici|axis|pnb|bob) bank",
            r"(?:amazon|flipkart|paytm|phonepe|gpay)",
            r"(?:google|microsoft|apple|facebook)",
            r"government (?:of india|official)",
            r"income tax (?:department|officer)",
            r"cyber (?:cell|crime|police)",
            r"rbi", r"sebi", r"uidai", r"epfo",
            r"customer (?:care|service|support) (?:executive|representative)",
            r"manager", r"officer", r"official", r"authorized"
        ]
        
        # Category 9: Phishing Link Indicators
        self.phishing_indicators = [
            r"click (?:here|this|link|below)",
            r"visit (?:this )?(?:link|website|url)",
            r"open (?:this )?(?:link|attachment)",
            r"download from", r"bit\.ly", r"tinyurl",
            r"ngrok\.io", r"herokuapp\.com",
            r"-(?:verify|secure|update|login|account)\.(?:com|in|net)",
            r"(?:verify|secure|update|login)-(?:account|now|here)"
        ]
        
        # Category 10: Indian Scam Specific
        self.indian_scam_keywords = [
            r"kyc (?:update|pending|expired)",
            r"aadhaar (?:link|update|verify)",
            r"pan (?:card|link|update|verify)",
            r"gst (?:registration|refund|notice)",
            r"lpg (?:subsidy|refund|booking)",
            r"ration card", r"voter (?:id|card)",
            r"pm (?:kisan|awas|yojana)",
            r"covid (?:relief|compensation|vaccine)",
            r"digital arrest", r"courier (?:scam|parcel)",
            r"customs (?:duty|clearance|notice)"
        ]
        
        # ============ Pattern Matching (Regex) ============
        
        self.patterns = {
            "upi_id": [
                r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}"
            ],
            "bank_account": [
                r"\b\d{9,18}\b",
                r"(?:account|ac|a/c)\s*[:#]?\s*(\d{4}[-\s]?\d{4}[-\s]?\d{4})",
                r"\b(?:IFSC|SWIFT)\b\s*[:#]?\s*[A-Z0-9]{4,11}"
            ],
            "phishing_link": [
                r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+",
                r"www\.[\w\-]+\.(?:com|in|net|org|co)",
                r"bit\.ly/[\w]+",
                r"tinyurl\.com/[\w]+"
            ],
            "phone_number": [
                r"\+91[-\s]?\d{10}",
                r"\b[6-9]\d{9}\b",
                r"\d{5}[-\s]?\d{5}"
            ],
            "otp_code": [
                r"\b\d{4,6}\b(?=.*(?:otp|code|pin|verification))"
            ],
            "amount": [
                r"(?:rs\.?|₹)\s*\d+(?:,\d{3})*(?:\.\d{2})?",
                r"\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:rupees?|rs\.?|₹)",
                r"\d+\s*(?:lakhs?|crores?)"
            ]
        }

    # ========================================================
    # 🎯 Advanced Scam Analysis
    # ========================================================

    def analyze(self, text: str) -> float:
        """
        Weighted scoring system for scam detection
        Returns: 0.0 to 1.0 (scam probability)
        """
        score = 0.0
        text_lower = text.lower()
        
        # Category weights (total = 1.0)
        weights = {
            "urgency": 0.15,
            "threat": 0.20,
            "legal": 0.20,
            "financial_lure": 0.10,
            "payment": 0.15,
            "tech_support": 0.15,
            "info_request": 0.20,
            "impersonation": 0.10,
            "phishing": 0.15,
            "indian_scam": 0.15
        }
        
        # Check each category
        categories_matched = []
        
        if self._check_keywords(text_lower, self.urgency_keywords):
            score += weights["urgency"]
            categories_matched.append("urgency")
        
        if self._check_keywords(text_lower, self.threat_keywords):
            score += weights["threat"]
            categories_matched.append("threat")
        
        if self._check_keywords(text_lower, self.legal_keywords):
            score += weights["legal"]
            categories_matched.append("legal")
        
        if self._check_keywords(text_lower, self.financial_lure_keywords):
            score += weights["financial_lure"]
            categories_matched.append("financial_lure")
        
        if self._check_keywords(text_lower, self.payment_keywords):
            score += weights["payment"]
            categories_matched.append("payment")
        
        if self._check_keywords(text_lower, self.tech_support_keywords):
            score += weights["tech_support"]
            categories_matched.append("tech_support")
        
        if self._check_keywords(text_lower, self.info_request_keywords):
            score += weights["info_request"]
            categories_matched.append("info_request")
        
        if self._check_keywords(text_lower, self.impersonation_keywords):
            score += weights["impersonation"]
            categories_matched.append("impersonation")
        
        if self._check_keywords(text_lower, self.phishing_indicators):
            score += weights["phishing"]
            categories_matched.append("phishing")
        
        if self._check_keywords(text_lower, self.indian_scam_keywords):
            score += weights["indian_scam"]
            categories_matched.append("indian_scam")
        
        # Bonus for multiple categories (indicates sophisticated scam)
        if len(categories_matched) >= 3:
            score += 0.1
        
        if len(categories_matched) >= 5:
            score += 0.15
        
        # Log detection
        if score > 0.5:
            logger.info(f"High scam score: {score:.2f}, Categories: {categories_matched}")
        
        return min(score, 1.0)
    
    def _check_keywords(self, text: str, keywords: list) -> bool:
        """Check if any keyword pattern matches"""
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in keywords)

    # ========================================================
    # 🔍 Entity Extraction
    # ========================================================

    def extract_entities(self, text: str) -> dict:
        """Extract scam-related entities from text"""
        return {
            "bankAccounts": self._extract_pattern(text, "bank_account"),
            "upiIds": self._extract_pattern(text, "upi_id"),
            "phishingLinks": self._extract_pattern(text, "phishing_link"),
            "phoneNumbers": self._extract_pattern(text, "phone_number"),
            "suspiciousKeywords": self._extract_suspicious_keywords(text)
        }
    
    def _extract_pattern(self, text: str, pattern_key: str) -> list:
        """Extract matches for a specific pattern"""
        matches = []
        if pattern_key in self.patterns:
            for pattern in self.patterns[pattern_key]:
                matches.extend([m.group() for m in re.finditer(pattern, text)])
        return list(set(matches))  # Remove duplicates
    
    def _extract_suspicious_keywords(self, text: str) -> list:
        """Extract all matched suspicious keywords"""
        keywords = []
        text_lower = text.lower()
        
        all_keyword_lists = [
            self.urgency_keywords,
            self.threat_keywords,
            self.legal_keywords,
            self.financial_lure_keywords,
            self.payment_keywords,
            self.tech_support_keywords,
            self.info_request_keywords,
            self.impersonation_keywords,
            self.phishing_indicators,
            self.indian_scam_keywords
        ]
        
        for keyword_list in all_keyword_lists:
            for pattern in keyword_list:
                if re.search(pattern, text_lower):
                    # Extract the actual matched text
                    match = re.search(pattern, text_lower)
                    if match:
                        keywords.append(match.group())
        
        return list(set(keywords))[:10]  # Return top 10 unique keywords

    # ========================================================
    # 📊 Detailed Analysis Report
    # ========================================================

    def get_detailed_analysis(self, text: str) -> dict:
        """Get comprehensive scam analysis report"""
        text_lower = text.lower()
        
        analysis = {
            "scam_score": self.analyze(text),
            "categories_detected": [],
            "risk_level": "low",
            "entities": self.extract_entities(text),
            "red_flags": []
        }
        
        # Detect categories
        if self._check_keywords(text_lower, self.urgency_keywords):
            analysis["categories_detected"].append("urgency_pressure")
            analysis["red_flags"].append("Uses urgency tactics")
        
        if self._check_keywords(text_lower, self.threat_keywords):
            analysis["categories_detected"].append("account_threat")
            analysis["red_flags"].append("Threatens account suspension")
        
        if self._check_keywords(text_lower, self.legal_keywords):
            analysis["categories_detected"].append("legal_threat")
            analysis["red_flags"].append("Uses legal intimidation")
        
        if self._check_keywords(text_lower, self.payment_keywords):
            analysis["categories_detected"].append("payment_request")
            analysis["red_flags"].append("Requests payment/money transfer")
        
        if self._check_keywords(text_lower, self.tech_support_keywords):
            analysis["categories_detected"].append("tech_support_scam")
            analysis["red_flags"].append("Requests remote access")
        
        if self._check_keywords(text_lower, self.info_request_keywords):
            analysis["categories_detected"].append("info_phishing")
            analysis["red_flags"].append("Requests sensitive information")
        
        # Determine risk level
        if analysis["scam_score"] >= 0.7:
            analysis["risk_level"] = "critical"
        elif analysis["scam_score"] >= 0.5:
            analysis["risk_level"] = "high"
        elif analysis["scam_score"] >= 0.3:
            analysis["risk_level"] = "medium"
        
        return analysis
