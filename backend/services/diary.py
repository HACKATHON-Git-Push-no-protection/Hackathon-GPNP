# services/diary.py
from repositories.diary import DiaryRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from models.diary import DiaryEntry

class DiaryService:
    def __init__(self, repo: DiaryRepository):
        self.repo = repo

    async def add_entry(self, note_text: str, recording: Optional[bytes]) -> DiaryEntry:
        return await self.repo.create(note_text, recording)

    async def get_entry(self, entry_id: int) -> Optional[DiaryEntry]:
        return await self.repo.get(entry_id)
