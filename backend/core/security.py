from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader, APIKey
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from core.config import get_settings

settings = get_settings()

# Password Context
# Using pbkdf2_sha256 to avoid bcrypt 72 byte limit
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")
    return encoded_jwt

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if settings.DEBUG:
        return api_key_header # Skip check in debug mode if needed, or strictly enforce
        
    if api_key_header == settings.API_KEY_SECRET:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
