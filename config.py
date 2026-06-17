import os
from typing import Optional
from pydantic import BaseModel


class Settings(BaseModel):
    # Telegram Bot Configuration
    bot_token: str = "7849871147:AAGj0-7ntpEs65FXbRm8AiU8WfbyH1MOGss"
    webhook_url: Optional[str] = None
    
    # Database Configuration
    database_url: str = "sqlite+aiosqlite:///./taro_bot.db"
    redis_url: str = "redis://localhost:6379/0"
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    
    # Payment Configuration
    payment_provider_token: Optional[str] = None
    
    # Admin Configuration
    admin_chat_id: Optional[int] = None
    
    # Application Settings
    debug: bool = True
    webhook_host: str = "0.0.0.0"
    webhook_port: int = 8000
    log_level: str = "INFO"
    
    # Timezone Settings
    default_timezone: str = "Asia/Almaty"
    
    # Subscription prices (in tenge)
    basic_subscription_price: int = 1000
    premium_subscription_price: int = 2500
    one_time_price: int = 300
    
settings = Settings() 