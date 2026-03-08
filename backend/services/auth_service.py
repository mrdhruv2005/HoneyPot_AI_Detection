from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from core.config import get_settings
from core.database import db
from models.user import UserInDB, TokenData

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
        
    users_collection = db.get_collection("users")
    user = await users_collection.find_one({"email": token_data.email})
    
    if user is None:
        raise credentials_exception
    return UserInDB(**user)
