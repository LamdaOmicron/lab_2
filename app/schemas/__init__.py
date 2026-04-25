"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
import uuid


# ============== User Schemas ==============

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserProfile(BaseModel):
    id: uuid.UUID
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ============== Character Schemas ==============

class CharacterCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: Optional[str] = Field(default='character', max_length=50)
    level: Optional[int] = Field(default=1, ge=1, le=20)
    class_name: Optional[str] = Field(default='', max_length=50)
    ancestry: Optional[str] = Field(default='', max_length=50)
    heritage: Optional[str] = Field(default='', max_length=100)
    background: Optional[str] = Field(default='', max_length=100)
    hp_max: Optional[int] = Field(default=15, ge=1)
    hp_current: Optional[int] = Field(default=15, ge=1)
    speed: Optional[int] = Field(default=25, ge=0)


class CharacterUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[str] = Field(None, max_length=50)
    level: Optional[int] = Field(None, ge=1, le=20)
    class_name: Optional[str] = Field(None, max_length=50)
    ancestry: Optional[str] = Field(None, max_length=50)
    heritage: Optional[str] = Field(None, max_length=100)
    background: Optional[str] = Field(None, max_length=100)
    hp_max: Optional[int] = Field(None, ge=1)
    hp_current: Optional[int] = Field(None, ge=1)
    speed: Optional[int] = Field(None, ge=0)


class CharacterResponse(BaseModel):
    id: uuid.UUID
    owner_id: uuid.UUID
    name: str
    type: str
    level: int
    class_name: Optional[str]
    ancestry: Optional[str]
    heritage: Optional[str]
    background: Optional[str]
    hp_max: int
    hp_current: int
    speed: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============== Pagination Schema ==============

class PaginationMeta(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int


class PaginatedCharacters(BaseModel):
    data: List[CharacterResponse]
    meta: PaginationMeta


# ============== OAuth Schemas ==============

class OAuthCallback(BaseModel):
    code: str
    state: Optional[str] = None
