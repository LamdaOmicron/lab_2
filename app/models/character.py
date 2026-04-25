"""
Character model.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base


class ActiveManager:
    """Mixin for filtering active (non-deleted) records."""
    
    @staticmethod
    def filter_active(query):
        return query.filter(BaseModel.deleted_at.is_(None))


class BaseModel:
    """Base mixin for common columns."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True, index=True)


class Character(Base, BaseModel):
    __tablename__ = 'characters'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    type = Column(String(50), default='character')  # character, npc, etc.
    level = Column(Integer, default=1, nullable=False)
    class_name = Column(String(50), nullable=True)
    ancestry = Column(String(50), nullable=True)
    heritage = Column(String(100), nullable=True)
    background = Column(String(100), nullable=True)
    hp_max = Column(Integer, default=15, nullable=False)
    hp_current = Column(Integer, default=15, nullable=False)
    speed = Column(Integer, default=25, nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="characters")
    
    def soft_delete(self):
        self.deleted_at = datetime.utcnow()
    
    def restore(self):
        self.deleted_at = None
    
    __table_args__ = (
        Index('ix_characters_deleted_at', 'deleted_at'),
        Index('ix_characters_name', 'name'),
    )
