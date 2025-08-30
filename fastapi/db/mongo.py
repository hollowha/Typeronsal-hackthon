# db/mongo.py
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL)

# 透過 URL 中的 /typersonal_db 自動對應
db = client.get_default_database()

async def get_db():
    return db
