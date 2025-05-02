# schemas/diary.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DiaryEntryCreate(BaseModel):
    note_text: str

class DiaryEntryRead(BaseModel):
    id: int
    created_at: datetime
    note_text: str
    recording: Optional[bytes] = None

    class Config:
        orm_mode = True
