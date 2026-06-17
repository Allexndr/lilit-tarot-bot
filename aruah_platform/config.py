"""
Конфигурация платформы АРУАХ
"""

import os
from typing import Optional
from pydantic import BaseModel


class Settings(BaseModel):
    # Telegram Bot Configuration
    bot_token: str = os.getenv("BOT_TOKEN", "")
    webhook_url: Optional[str] = os.getenv("WEBHOOK_URL")
    
    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "postgresql://aruah:aruah123@localhost:5432/aruah_db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # AI Services
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Payment Systems
    robokassa_login: str = os.getenv("ROBOKASSA_LOGIN", "")
    robokassa_password1: str = os.getenv("ROBOKASSA_PASSWORD1", "")
    robokassa_password2: str = os.getenv("ROBOKASSA_PASSWORD2", "")
    robokassa_test_mode: bool = os.getenv("ROBOKASSA_TEST_MODE", "true").lower() == "true"
    
    # Application Settings
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    secret_key: str = os.getenv("SECRET_KEY", "aruah_secret_key_2024")
    
    # Admin
    admin_chat_id: Optional[int] = int(os.getenv("ADMIN_CHAT_ID", "0")) if os.getenv("ADMIN_CHAT_ID") else None
    admin_email: str = os.getenv("ADMIN_EMAIL", "admin@aruah.kz")
    
    # Timezone
    default_timezone: str = os.getenv("DEFAULT_TIMEZONE", "Asia/Almaty")
    
    # Subscription Prices (in KZT)
    free_daily_limit: int = int(os.getenv("FREE_DAILY_LIMIT", "3"))
    premium_price: int = int(os.getenv("PREMIUM_PRICE", "2500"))
    vip_consultation_price: int = int(os.getenv("VIP_CONSULTATION_PRICE", "15000"))
    
    # File Storage
    aws_access_key_id: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_bucket_name: str = os.getenv("AWS_BUCKET_NAME", "aruah-files")
    aws_region: str = os.getenv("AWS_REGION", "eu-west-1")


settings = Settings()

