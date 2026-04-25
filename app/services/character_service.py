"""
Character service for CRUD operations.
"""
import uuid
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.character import Character
from app.middleware.exceptions import NotFoundError, ConflictError


class CharacterService:
    @staticmethod
    def get_all_active(db: Session, page: int = 1, limit: int = 10, owner_id: Optional[uuid.UUID] = None) -> Dict[str, Any]:
        """Get all active characters with pagination."""
        query = db.query(Character).filter(Character.deleted_at.is_(None))
        
        # Filter by owner if provided
        if owner_id:
            query = query.filter(Character.owner_id == owner_id)
        
        total = query.count()
        offset = (page - 1) * limit
        items = query.offset(offset).limit(limit).all()
        
        total_pages = (total + limit - 1) // limit if limit > 0 else 1
        
        return {
            'data': items,
            'meta': {
                'total': total,
                'page': page,
                'limit': limit,
                'total_pages': total_pages,
            }
        }
    
    @staticmethod
    def get_by_id(db: Session, character_id: uuid.UUID, owner_id: Optional[uuid.UUID] = None) -> Optional[Character]:
        """Get character by ID."""
        query = db.query(Character).filter(
            Character.id == character_id,
            Character.deleted_at.is_(None)
        )
        
        if owner_id:
            query = query.filter(Character.owner_id == owner_id)
        
        return query.first()
    
    @staticmethod
    def create(db: Session, data: Dict[str, Any], owner_id: uuid.UUID) -> Character:
        """Create a new character."""
        # Check for name conflict within user's characters
        existing = db.query(Character).filter(
            Character.name == data['name'],
            Character.owner_id == owner_id,
            Character.deleted_at.is_(None)
        ).first()
        
        if existing:
            raise ConflictError("Character with this name already exists")
        
        character = Character(
            owner_id=owner_id,
            **data
        )
        db.add(character)
        db.commit()
        db.refresh(character)
        return character
    
    @staticmethod
    def update(db: Session, character_id: uuid.UUID, data: Dict[str, Any], owner_id: uuid.UUID, partial: bool = False) -> Character:
        """Update a character."""
        character = db.query(Character).filter(
            Character.id == character_id,
            Character.owner_id == owner_id,
            Character.deleted_at.is_(None)
        ).first()
        
        if not character:
            raise NotFoundError("Character not found")
        
        # Check for name conflict if name is changing
        if 'name' in data and data['name'] != character.name:
            existing = db.query(Character).filter(
                Character.name == data['name'],
                Character.owner_id == owner_id,
                Character.id != character_id,
                Character.deleted_at.is_(None)
            ).first()
            
            if existing:
                raise ConflictError("Character with this name already exists")
        
        # Update fields
        for key, value in data.items():
            if hasattr(character, key):
                setattr(character, key, value)
        
        db.commit()
        db.refresh(character)
        return character
    
    @staticmethod
    def delete(db: Session, character_id: uuid.UUID, owner_id: uuid.UUID) -> bool:
        """Soft delete a character."""
        character = db.query(Character).filter(
            Character.id == character_id,
            Character.owner_id == owner_id,
            Character.deleted_at.is_(None)
        ).first()
        
        if not character:
            raise NotFoundError("Character not found")
        
        character.soft_delete()
        db.commit()
        return True
