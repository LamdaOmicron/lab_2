"""
Auth router for user registration, login, and token management.
"""
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.auth_service import AuthService
from app.schemas import UserRegister, UserLogin, UserProfile, TokenResponse
from app.middleware.auth import get_current_user
from datetime import timedelta

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(response: Response, data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user."""
    user, access_token, refresh_token = AuthService.register(
        db=db,
        email=data.email,
        password=data.password
    )
    
    # Set cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=int(timedelta(minutes=15).total_seconds())
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(timedelta(minutes=10080).total_seconds())
    )
    
    return UserProfile(
        id=user.id,
        email=user.email,
        created_at=user.created_at
    )


@router.post("/login")
def login(response: Response, data: UserLogin, db: Session = Depends(get_db)):
    """Login user."""
    user, access_token, refresh_token = AuthService.login(
        db=db,
        email=data.email,
        password=data.password
    )
    
    # Set cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(timedelta(minutes=15).total_seconds())
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(timedelta(minutes=10080).total_seconds())
    )
    
    return UserProfile(
        id=user.id,
        email=user.email,
        created_at=user.created_at
    )


@router.post("/refresh")
def refresh(response: Response, request_token: str = None, db: Session = Depends(get_db)):
    """Refresh access token."""
    # In real implementation, get from cookie
    if not request_token:
        return {"error": "Refresh token required"}
    
    new_access, new_refresh = AuthService.refresh(db=db, refresh_token=request_token)
    
    response.set_cookie(
        key="access_token",
        value=new_access,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(timedelta(minutes=15).total_seconds())
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(timedelta(minutes=10080).total_seconds())
    )
    
    return {"message": "Token refreshed"}


@router.post("/logout")
def logout(response: Response, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Logout user."""
    # Get refresh token from cookie (implementation depends on framework)
    AuthService.logout(db=db, refresh_token="")  # Should get from cookie
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}


@router.get("/me")
def who_am_i(current_user: dict = Depends(get_current_user)):
    """Get current user info."""
    return current_user
