from fastapi import APIRouter, Depends, HTTPException, Request, status

from ..config import Settings
from ..schemas import LoginRequest, Token
from ..security import authenticate, create_access_token, require_admin, require_auth_configured

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=Token, responses={429: {"description": "Too many failed attempts"}})
def login(payload: LoginRequest, request: Request, settings: Settings = Depends(require_auth_configured)):
    """Exchange the admin username and password for a short-lived JWT.

    Failed attempts are limited per client IP to slow down password guessing.
    """
    limiter = request.app.state.login_limiter
    client = request.client.host if request.client else "unknown"
    wait = limiter.retry_after(client)
    if wait:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed login attempts, try again later",
            headers={"Retry-After": str(wait)},
        )
    if not authenticate(payload.username, payload.password, settings):
        limiter.record_failure(client)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    limiter.reset(client)
    return Token(
        access_token=create_access_token(payload.username, settings),
        expires_in=settings.jwt_expire_minutes * 60,
    )


@router.get("/me")
def me(username: str = Depends(require_admin)):
    return {"username": username}
