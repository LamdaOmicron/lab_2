"""
Character router for CRUD operations.
"""
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.services.character_service import CharacterService
from app.schemas import CharacterCreate, CharacterUpdate, CharacterResponse, PaginatedCharacters
from app.middleware.auth import get_current_user
import uuid

router = APIRouter(prefix="/api/characters", tags=["Characters"])


@router.get("", response_model=PaginatedCharacters)
def get_characters(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100)
):
    """Get all active characters with pagination."""
    owner_id = uuid.UUID(current_user["user_id"])
    result = CharacterService.get_all_active(
        db=db,
        page=page,
        limit=min(limit, 100),
        owner_id=owner_id
    )
    return result


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CharacterResponse)
def create_character(
    data: CharacterCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new character."""
    owner_id = uuid.UUID(current_user["user_id"])
    character = CharacterService.create(
        db=db,
        data=data.model_dump(exclude_unset=True),
        owner_id=owner_id
    )
    return character


@router.get("/{character_id}", response_model=CharacterResponse)
def get_character(
    character_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get character by ID."""
    owner_id = uuid.UUID(current_user["user_id"])
    character = CharacterService.get_by_id(
        db=db,
        character_id=uuid.UUID(character_id),
        owner_id=owner_id
    )
    if not character:
        from app.middleware.exceptions import NotFoundError
        raise NotFoundError("Character not found")
    return character


@router.put("/{character_id}", response_model=CharacterResponse)
def update_character(
    character_id: str,
    data: CharacterUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Fully update a character."""
    owner_id = uuid.UUID(current_user["user_id"])
    character = CharacterService.update(
        db=db,
        character_id=uuid.UUID(character_id),
        data=data.model_dump(exclude_unset=True),
        owner_id=owner_id,
        partial=False
    )
    return character


@router.patch("/{character_id}", response_model=CharacterResponse)
def patch_character(
    character_id: str,
    data: CharacterUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Partially update a character."""
    owner_id = uuid.UUID(current_user["user_id"])
    character = CharacterService.update(
        db=db,
        character_id=uuid.UUID(character_id),
        data=data.model_dump(exclude_unset=True),
        owner_id=owner_id,
        partial=True
    )
    return character


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(
    character_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Soft delete a character."""
    owner_id = uuid.UUID(current_user["user_id"])
    CharacterService.delete(
        db=db,
        character_id=uuid.UUID(character_id),
        owner_id=owner_id
    )
    return None
