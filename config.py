import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram
    TOKEN_MODERATION_BOT = os.getenv("TOKEN_MODERATION_BOT")
    MODERATOR_CHAT_ID = int(os.getenv("MODERATOR_CHAT_ID"))
    PUBLIC_CHANNEL_ID = int(os.getenv("PUBLIC_CHANNEL_ID"))
    
    # Redis
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    REDIS_SSL = os.getenv("REDIS_SSL", "False").lower() in ("true", "1")
    REDIS_TTL = 24 * 60 * 60