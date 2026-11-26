from fastapi import APIRouter, Depends, HTTPException, status

from ..config import Settings
from ..schemas import LoginRequest, Token
from ..security import authenticate, create_access_token, require_admin, require_auth_configured

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, settings: Settings = Depends(require_auth_configured)):
    """Exchange the admin username and password for a short-lived JWT."""
    if not authenticate(payload.username, payload.password, settings):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return Token(
        access_token=create_access_token(payload.username, settings),
        expires_in=settings.jwt_expire_minutes * 60,
    )


@router.get("/me")
def me(username: str = Depends(require_admin)):
    return {"username": username}
