from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class EPGProgram(BaseModel):
    channel_id: str = Field(..., description="Channel ID")
    title: str = Field(..., description="Program title")
    description: Optional[str] = Field(None, description="Program description")
    start_time: datetime = Field(..., description="Program start time")
    end_time: datetime = Field(..., description="Program end time")
    category: Optional[str] = Field(None, description="Program category")
    icon: Optional[str] = Field(None, description="Program icon URL")
    
    @property
    def duration_minutes(self) -> int:
        return int((self.end_time - self.start_time).total_seconds() / 60)
    
    class Config:
        json_schema_extra = {
            "example": {
                "channel_id": "tv3",
                "title": "News at 8",
                "description": "Evening news bulletin",
                "start_time": "2024-01-01T20:00:00",
                "end_time": "2024-01-01T21:00:00",
                "category": "News"
            }
        }


class EPGResponse(BaseModel):
    programs: List[EPGProgram]
    channel_id: Optional[str] = None
    total: int


class EPGChannelPrograms(BaseModel):
    channel_id: str
    channel_name: str
    current_program: Optional[EPGProgram] = None
    upcoming_programs: List[EPGProgram] = []
