from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Favorite(BaseModel):
    channel_id: str = Field(..., description="Channel ID")
    added_at: datetime = Field(default_factory=datetime.utcnow, description="When favorite was added")
    list_name: Optional[str] = Field(default="default", description="Custom list name")
    
    
class FavoriteRequest(BaseModel):
    channel_id: str = Field(..., description="Channel ID to add")
    list_name: Optional[str] = Field(default="default", description="Custom list name")


class FavoriteResponse(BaseModel):
    favorites: List[str]
    total: int
    list_name: str
    
    
class FavoriteListsResponse(BaseModel):
    lists: List[str]
    total: int
