from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Literal
from datetime import datetime

# Enums
class SenderType(str):
    SCAMMER = "scammer"
    USER = "user"

class ChannelType(str):
    SMS = "SMS"
    WHATSAPP = "WhatsApp"
    EMAIL = "Email"
    CHAT = "Chat"

# Sub-models
class Message(BaseModel):
    sender: str
    text: str
    timestamp: datetime

class ConversationItem(BaseModel):
    sender: str
    text: str
    timestamp: datetime

class Metadata(BaseModel):
    channel: str = "SMS"
    language: str = "English"
    locale: str = "IN"

# Main Request
class ScamMessageRequest(BaseModel):
    sessionId: str = Field(..., min_length=5)
    message: Message
    conversationHistory: List[ConversationItem] = []
    metadata: Optional[Metadata] = None

# Response Models
class IntelligenceData(BaseModel):
    bankAccounts: List[str] = []
    upiIds: List[str] = []
    phishingLinks: List[str] = []
    phoneNumbers: List[str] = []
    suspiciousKeywords: List[str] = []

class AgentResponse(BaseModel):
    status: str = "success"
    reply: str
    riskScore: float = 0.0
    scamDetected: bool = False
    extractedIntelligence: Optional[IntelligenceData] = None

class FinalCallbackPayload(BaseModel):
    sessionId: str
    scamDetected: bool
    totalMessagesExchanged: int
    extractedIntelligence: IntelligenceData
    agentNotes: str
