import redis
import json
from datetime import datetime, timedelta
from typing import List, Dict
from core.config import get_settings
from models.schemas import Message, IntelligenceData

settings = get_settings()

class SessionManager:
    def __init__(self):
        # In Docker, hostname is 'redis'. Localhost for fallback.
        try:
            self.redis = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
            self.redis.ping()
        except redis.ConnectionError:
            print("WARNING: Redis connection failed. Session persistence disabled.")
            self.redis = None

    def get_session(self, user_id: str, session_id: str) -> Dict:
        if not self.redis: return {}
        # Key: session:{user_id}:{session_id}
        data = self.redis.get(f"session:{user_id}:{session_id}")
        return json.loads(data) if data else {}

    def save_session(self, user_id: str, session_id: str, history: List[dict], intelligence: dict):
        if not self.redis: return
        data = {
            "history": history,
            "intelligence": intelligence,
            "updated_at": datetime.now().isoformat()
        }
        # Expire after 24 hours
        self.redis.setex(f"session:{user_id}:{session_id}", timedelta(hours=24), json.dumps(data, default=str))

    def add_message(self, user_id: str, session_id: str, message: dict):
        if not self.redis: return
        session = self.get_session(user_id, session_id)
        history = session.get("history", [])
        history.append(message)
        
        # Sliding Window (Keep last 20 messages)
        if len(history) > 20: 
            history = history[-20:]
            
        intelligence = session.get("intelligence", {})
        self.save_session(user_id, session_id, history, intelligence)

    def update_intelligence(self, user_id: str, session_id: str, new_intel: dict):
        if not self.redis: return
        session = self.get_session(user_id, session_id)
        current_intel = session.get("intelligence", {
            "bankAccounts": [], "upiIds": [], "phishingLinks": [], 
            "phoneNumbers": [], "suspiciousKeywords": []
        })
        
        # Merge lists roughly
        for key in current_intel:
            if key in new_intel:
                current_intel[key] = list(set(current_intel[key] + new_intel.get(key, [])))
                
        self.save_session(user_id, session_id, session.get("history", []), current_intel)

    def update_session_batch(self, user_id: str, session_id: str, message: dict = None, new_intel: dict = None):
        """
        Consolidated update method to minimize Redis round-trips.
        Fetches session once, updates history and intel, and saves once.
        Returns the updated session object.
        """
        if not self.redis: return {}
        
        # 1. Fetch Session (Read)
        session = self.get_session(user_id, session_id)
        
        # 2. Update History
        history = session.get("history", [])
        if message:
            history.append(message)
            # Sliding Window
            if len(history) > 20: history = history[-20:]
            
        # 3. Update Intelligence
        current_intel = session.get("intelligence", {
            "bankAccounts": [], "upiIds": [], "phishingLinks": [], 
            "phoneNumbers": [], "suspiciousKeywords": []
        })
        if new_intel:
            for key in current_intel:
                if key in new_intel:
                    current_intel[key] = list(set(current_intel[key] + new_intel.get(key, [])))
                    
        # 4. Save Session (Write)
        self.save_session(user_id, session_id, history, current_intel)
        
        # Return updated structure locally
        return {
            "history": history,
            "intelligence": current_intel
        }

    def increment_stats(self, user_id: str, key: str, amount: int = 1):
        if not self.redis: return
        # User Scoped Stats: stats:{user_id}:{key}
        self.redis.incrby(f"stats:{user_id}:{key}", amount)
        
        # Track hourly activity for charts (User Scoped)
        current_hour = datetime.now().strftime("%H:00")
        self.redis.hincrby(f"stats:{user_id}:activity:{current_hour}", key, amount)
        self.redis.expire(f"stats:{user_id}:activity:{current_hour}", timedelta(hours=48))

    def get_dashboard_stats(self, user_id: str):
        if not self.redis: 
            return {
                "totalMessages": 0,
                "scamsDetected": 0,
                "bankAccountsExtracted": 0,
                "upiIdsExtracted": 0,
                "phishingLinksExtracted": 0,
                "phoneNumbersExtracted": 0,
                "activityData": []
            }
            
        total_msgs = int(self.redis.get(f"stats:{user_id}:total_messages") or 0)
        scams = int(self.redis.get(f"stats:{user_id}:scams_detected") or 0)
        bank_accounts = int(self.redis.get(f"stats:{user_id}:bank_accounts_extracted") or 0)
        upi_ids = int(self.redis.get(f"stats:{user_id}:upi_ids_extracted") or 0)
        phishing_links = int(self.redis.get(f"stats:{user_id}:phishing_links_extracted") or 0)
        phone_numbers = int(self.redis.get(f"stats:{user_id}:phone_numbers_extracted") or 0)
        
        # reconstruct activity data for last 24h
        activity_data = []
        now = datetime.now()
        # Use pipeline to fetch 24 hours of data in 1 network call
        pipeline = self.redis.pipeline()
        time_slots = []
        now = datetime.now()
        
        for i in range(23, -1, -1):
            time_slot = (now - timedelta(hours=i)).strftime("%H:00")
            time_slots.append(time_slot)
            pipeline.hgetall(f"stats:{user_id}:activity:{time_slot}")
            
        # Execute batch
        results = pipeline.execute()
        
        # Build activity data from batch results
        activity_data = []
        for time_slot, data in zip(time_slots, results):
            activity_data.append({
                "time": time_slot,
                "scams": int(data.get("scams_detected", 0)),
                "safe": int(data.get("safe_messages", 0)) 
            })
            
        # Get Recent Activity
        recent_activity_raw = self.redis.lrange(f"recent_activity:{user_id}", 0, 9)
        recent_activity = [json.loads(x) for x in recent_activity_raw] if recent_activity_raw else []
            
        return {
            "totalMessages": total_msgs,
            "scamsDetected": scams,
            "bankAccountsExtracted": bank_accounts,
            "upiIdsExtracted": upi_ids,
            "phishingLinksExtracted": phishing_links,
            "phoneNumbersExtracted": phone_numbers,
            "activityData": activity_data,
            "recentActivity": recent_activity
        }

    def log_recent_activity(self, user_id: str, activity: dict):
        """
        Log recent activity for the dashboard feed.
        activity = {
            "sessionId": "...",
            "snippet": "...",
            "timestamp": "...",
            "status": "SAFE" | "SCAM"
        }
        """
        if not self.redis: return
        
        # Add to list (Left Push)
        self.redis.lpush(f"recent_activity:{user_id}", json.dumps(activity))
        # Keep only last 10 items (Trim)
        self.redis.ltrim(f"recent_activity:{user_id}", 0, 9)

    def batch_update_stats(self, user_id: str, updates: Dict[str, int]):
        """
        Batch update multiple stats using a Redis pipeline for performance.
        updates = {"total_messages": 1, "scams_detected": 1, ...}
        """
        if not self.redis: return
        
        pipeline = self.redis.pipeline()
        current_hour = datetime.now().strftime("%H:00")
        
        for key, amount in updates.items():
            # User Scoped Stats
            pipeline.incrby(f"stats:{user_id}:{key}", amount)
            
            # Hourly Activity
            pipeline.hincrby(f"stats:{user_id}:activity:{current_hour}", key, amount)
            
        # Set expiry for hourly stats (only needs to be done once per batch really, but harmless here)
        pipeline.expire(f"stats:{user_id}:activity:{current_hour}", timedelta(hours=48))
        
        # Execute all commands in one network round-trip
        try:
            pipeline.execute()
        except Exception as e:
            print(f"Error in batch stats update: {e}")
