from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.schemas import UserAuth, Token
from app.core.security import create_access_token, get_password_hash, verify_password
from typing import Dict

router = APIRouter(prefix="/auth", tags=["auth"])

# Mock DB for demonstration - using lazy-loaded password hash
_MOCK_USER_DB_CACHE = None

def get_mock_user_db():
    global _MOCK_USER_DB_CACHE
    if _MOCK_USER_DB_CACHE is None:
        _MOCK_USER_DB_CACHE = {
            "testuser": {
                "username": "testuser",
                "hashed_password": get_password_hash("password123")
            }
        }
    return _MOCK_USER_DB_CACHE

MOCK_USER_DB = property(lambda self: get_mock_user_db())

@router.post("/init-session", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = get_mock_user_db()
    user = user_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
