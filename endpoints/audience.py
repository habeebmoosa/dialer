from fastapi import APIRouter, Path
import requests
import os

router = APIRouter()

HUME_API_KEY = os.getenv("HUME_API_KEY")
    

@router.get("/get_chat/{chat_id}")
def get_chat_by_id(chat_id: str = Path(...)):
    response = requests.get(
        f"https://api.hume.ai/v0/evi/chats/{chat_id}?page_number=0&page_size=100&ascending_order=true",
        headers={
            "X-Hume-Api-Key": HUME_API_KEY
        },
        )
    
    data = response.json()

    filtered_events = [
    {
        "id": event["id"],
        "chat_id": event["chat_id"],
        "role": event["role"],
        "timestamp": event["timestamp"],
        "type": event["type"],
        "message_text": event["message_text"]
    }
    for event in data.get("events_page", [])[1:]
    ]
    
    data["events_page"] = filtered_events
    
    return data


@router.get("/list_chat")
def list_chats():
    response = requests.get(
        f"https://api.hume.ai/v0/evi/chats?page_number=0&page_size=23&ascending_order=true",
        headers={
            "X-Hume-Api-Key": HUME_API_KEY
        },
        )
    
    data = response.json()
    return data


@router.get("/get_audio/{chat_id}")
def get_chat_audio(chat_id: str):
    response = requests.get(
        f"https://api.hume.ai/v0/evi/chats/{chat_id}/audio",
        headers={
            "X-Hume-Api-Key": HUME_API_KEY
        },
    )

    return response.json()
