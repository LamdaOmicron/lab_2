"""
User and RefreshToken models.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(200), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=True)  # bcrypt hash
    
    # OAuth identifiers
    yandex_id = Column(String(100), unique=True, nullable=True, index=True)
    vk_id = Column(String(100), unique=True, nullable=True, index=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True, index=True)
    
    # Relationships
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    characters = relationship("Character", back_populates="owner", cascade="all, delete-orphan")
    
    @property
    def is_active(self):
        return self.deleted_at is None
    
    def soft_delete(self):
        self.deleted_at = datetime.utcnow()
    
    def restore(self):
        self.deleted_at = None
    
    def set_password(self, raw_password: str):
        """Hash password with bcrypt."""
        if not raw_password:
            self.password = None
            return
        import bcrypt
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(raw_password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, raw_password: str) -> bool:
        """Check password against stored hash."""
        if not self.password:
            return False
        import bcrypt
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))
    
    def __repr__(self):
        return f"<User(email={self.email})>"


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    token_hash = Column(String(128), nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="refresh_tokens")
    
    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at
    
    def revoke(self):
        self.revoked = True
    
    __table_args__ = (
        Index('ix_refresh_tokens_user_revoked', 'user_id', 'revoked'),
    )
