"""
Auth service for user registration, login, token management.
"""
import uuid
import jwt
import hashlib
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.user import User, RefreshToken
from app.config import get_settings
from app.middleware.exceptions import AuthenticationError, ConflictError

settings = get_settings()


class AuthService:
    @staticmethod
    def register(db: Session, email: str, password: str) -> tuple[User, str, str]:
        """Register a new user."""
        # Check if user exists
        existing_user = db.query(User).filter(
            User.email == email,
            User.deleted_at.is_(None)
        ).first()
        
        if existing_user:
            raise ConflictError("User with this email already exists")
        
        # Create new user
        user = User(email=email)
        user.set_password(password)
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Generate tokens
        access_token = AuthService._create_access_token(user)
        refresh_token = AuthService._create_refresh_token(user)
        
        # Store refresh token hash
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        expires_at = datetime.utcnow() + timedelta(minutes=settings.JWT_REFRESH_EXPIRATION)
        refresh_token_obj = RefreshToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at
        )
        db.add(refresh_token_obj)
        db.commit()
        
        return user, access_token, refresh_token
    
    @staticmethod
    def login(db: Session, email: str, password: str) -> tuple[User, str, str]:
        """Login user."""
        user = db.query(User).filter(
            User.email == email,
            User.deleted_at.is_(None)
        ).first()
        
        if not user or not user.check_password(password):
            raise AuthenticationError("Invalid email or password")
        
        # Generate tokens
        access_token = AuthService._create_access_token(user)
        refresh_token = AuthService._create_refresh_token(user)
        
        # Store refresh token hash
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        expires_at = datetime.utcnow() + timedelta(minutes=settings.JWT_REFRESH_EXPIRATION)
        refresh_token_obj = RefreshToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at
        )
        db.add(refresh_token_obj)
        db.commit()
        
        return user, access_token, refresh_token
    
    @staticmethod
    def refresh(db: Session, refresh_token: str) -> tuple[str, str]:
        """Refresh access token."""
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        
        token_obj = db.query(RefreshToken).filter(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked == False
        ).first()
        
        if not token_obj or token_obj.is_expired():
            raise AuthenticationError("Invalid or expired refresh token")
        
        user = db.query(User).filter(
            User.id == token_obj.user_id,
            User.deleted_at.is_(None)
        ).first()
        
        if not user:
            raise AuthenticationError("User not found")
        
        # Revoke old token
        token_obj.revoke()
        
        # Generate new tokens
        new_access = AuthService._create_access_token(user)
        new_refresh = AuthService._create_refresh_token(user)
        
        # Store new refresh token
        new_token_hash = hashlib.sha256(new_refresh.encode()).hexdigest()
        expires_at = datetime.utcnow() + timedelta(minutes=settings.JWT_REFRESH_EXPIRATION)
        new_token_obj = RefreshToken(
            user_id=user.id,
            token_hash=new_token_hash,
            expires_at=expires_at
        )
        db.add(new_token_obj)
        db.commit()
        
        return new_access, new_refresh
    
    @staticmethod
    def logout(db: Session, refresh_token: str):
        """Logout by revoking refresh token."""
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        token_obj = db.query(RefreshToken).filter(
            RefreshToken.token_hash == token_hash
        ).first()
        
        if token_obj:
            token_obj.revoke()
            db.commit()
    
    @staticmethod
    def logout_all(db: Session, user_id: uuid.UUID):
        """Logout all sessions for a user."""
        db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id
        ).update({"revoked": True})
        db.commit()
    
    @staticmethod
    def _create_access_token(user: User) -> str:
        """Create JWT access token."""
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_EXPIRATION),
            "type": "access"
        }
        return jwt.encode(payload, settings.JWT_ACCESS_SECRET, algorithm="HS256")
    
    @staticmethod
    def _create_refresh_token(user: User) -> str:
        """Create JWT refresh token (for client-side storage reference)."""
        payload = {
            "sub": str(user.id),
            "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_REFRESH_EXPIRATION),
            "type": "refresh"
        }
        return jwt.encode(payload, settings.JWT_REFRESH_SECRET, algorithm="HS256")
