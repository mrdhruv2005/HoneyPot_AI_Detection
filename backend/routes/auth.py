from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from core.database import db
from core.security import verify_password, get_password_hash, create_access_token
from models.user import UserCreate, UserInDB, Token
from datetime import datetime

router = APIRouter(tags=["Authentication"])

@router.post("/signup", response_model=dict)
async def signup(user: UserCreate):
    users_collection = db.get_collection("users")
    
    # Check if email exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    hashed_password = get_password_hash(user.password)
    
    new_user = {
        "name": user.name,
        "email": user.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }
    
    result = await users_collection.insert_one(new_user)
    
    return {
        "id": str(result.inserted_id),
        "name": user.name,
        "email": user.email
    }

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2PasswordRequestForm uses 'username' field, but we assume it contains the email
    email = form_data.username
    password = form_data.password
    
    users_collection = db.get_collection("users")
    user = await users_collection.find_one({"email": email})
    
    if not user:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not verify_password(password, user["hashed_password"]):
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(
        data={"sub": user["email"]} # Use email as subject
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
