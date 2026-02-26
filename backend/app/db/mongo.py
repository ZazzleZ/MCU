from app.core.config import mongodb_url, mongodb_db
from motor.motor_asyncio import AsyncIOMotorClient


client = AsyncIOMotorClient(mongodb_url)
db = client[mongodb_db]


