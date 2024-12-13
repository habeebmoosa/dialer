from fastapi import APIRouter, UploadFile, File, HTTPException, Path
import os

from services.hume import HumeService

hume_service = HumeService()

router = APIRouter()

HUME_API_KEY = os.getenv("HUME_API_KEY")

@router.get("/transcript/{chat_id}")
def get_chat_by_id(chat_id: str = Path(...)):
    if not chat_id:
        return None
    
    return hume_service.get_chat_transcript(chat_id)


@router.get("/list_chat")
def list_chats(user_id: str):
    if not user_id:
        return None
    
    return hume_service.list_of_chats_history(user_id)


@router.get("/get_audio/{chat_id}")
def get_chat_audio(chat_id: str):
    if not chat_id:
        return None
    
    return hume_service.get_chat_audio(chat_id)