# repositories/diary.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert
from models.diary import DiaryEntry
from typing import Optional, Dict, Any

class DiaryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, note_text: str, recording: Optional[bytes]) -> DiaryEntry:
        stmt = (
            insert(DiaryEntry)
            .values(note_text=note_text, recording=recording)
            .returning(DiaryEntry)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get(self, entry_id: int) -> Optional[DiaryEntry]:
        stmt = select(DiaryEntry).where(DiaryEntry.id == entry_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(
        self, entry_id: int, fields: Dict[str, Any]
    ) -> Optional[DiaryEntry]:
        stmt = (
            update(DiaryEntry)
            .where(DiaryEntry.id == entry_id)
            .values(**fields)
            .returning(DiaryEntry)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()
