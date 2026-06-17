from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import hashlib
import hmac
import json
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from config import settings
from bot.services import UserService
from bot.models import User

# Configuration
SECRET_KEY = settings.bot_token  # Using bot token as secret for simplicity, or generate a specific one
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

def verify_telegram_auth(data: Dict[str, Any], bot_token: str) -> bool:
    """
    Verifies the integrity of the data received from the Telegram Login Widget.
    Reference: https://core.telegram.org/widgets/login#checking-authorization
    """
    if "hash" not in data:
        return False

    received_hash = data["hash"]
    auth_data = data.copy()
    del auth_data["hash"]

    # Sort keys alphabetically and create data-check-string
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(auth_data.items()))
    
    # Compute the secret key: SHA256 of the bot token
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    
    # Compute the hash of the data-check-string using the secret key
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    return computed_hash == received_hash

def check_auth_date(auth_date: int) -> bool:
    """Check if auth data is not too old (e.g. < 24 hours)"""
    now = datetime.now().timestamp()
    return (now - int(auth_date)) < 86400

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
        
    user = await UserService.get_or_create_user(telegram_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user
