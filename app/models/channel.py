from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime


class Channel(BaseModel):
    id: str = Field(..., description="Unique channel identifier")
    name: str = Field(..., description="Channel name")
    logo: Optional[str] = Field(None, description="Channel logo URL")
    group: Optional[str] = Field(None, description="Channel group/category")
    url: str = Field(..., description="Stream URL")
    epg_id: Optional[str] = Field(None, description="EPG channel ID")
    language: Optional[str] = Field(None, description="Channel language")
    country: str = Field(default="MY", description="Country code")
    tvg_id: Optional[str] = Field(None, description="TVG ID")
    tvg_name: Optional[str] = Field(None, description="TVG Name")
    radio: bool = Field(default=False, description="Is radio channel")
    is_astro: bool = Field(default=False, description="Is Astro channel")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "tv3",
                "name": "TV3",
                "logo": "https://example.com/tv3.png",
                "group": "News",
                "url": "https://stream.example.com/tv3.m3u8",
                "epg_id": "TV3.my",
                "language": "Malay",
                "country": "MY",
                "is_astro": False
            }
        }


class ChannelResponse(BaseModel):
    channels: List[Channel]
    total: int
    page: int
    page_size: int
    
    
class ChannelSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Search query")
    

class ChannelGroupsResponse(BaseModel):
    groups: List[str]
    total: int
