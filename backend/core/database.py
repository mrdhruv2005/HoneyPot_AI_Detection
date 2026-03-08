from motor.motor_asyncio import AsyncIOMotorClient
from core.config import get_settings
import logging

settings = get_settings()
logger = logging.getLogger("database")

class Database:
    client: AsyncIOMotorClient = None
    db_name = "erp_db"

    def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGO_URI)
            logger.info("Connected to MongoDB Atlas")
        except Exception as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise e

    def get_db(self):
        return self.client[self.db_name]
    
    def get_collection(self, collection_name: str):
        return self.client[self.db_name][collection_name]

    def close(self):
        if self.client:
            self.client.close()

db = Database()
