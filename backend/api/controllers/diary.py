# api/diary.py
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session
from repositories.diary import DiaryRepository
from services.diary import DiaryService
from schemas.diary import DiaryEntryCreate, DiaryEntryRead

router = APIRouter(prefix="/diary", tags=["Diary"])

def get_service(session: AsyncSession = Depends(get_session)) -> DiaryService:
    repo = DiaryRepository(session)
    return DiaryService(repo)

@router.post("/", response_model=DiaryEntryRead)
async def create_diary(
    note_text: str = Form(...),
    recording: UploadFile = File(None),
    svc: DiaryService = Depends(get_service),
):
    data = await recording.read() if recording else None
    entry = await svc.add_entry(note_text, data)
    return entry

@router.get("/{entry_id}", response_model=DiaryEntryRead)
async def read_diary(entry_id: int, svc: DiaryService = Depends(get_service)):
    entry = await svc.get_entry(entry_id)
    if not entry:
        raise HTTPException(404, "Entry not found")
    return entry
