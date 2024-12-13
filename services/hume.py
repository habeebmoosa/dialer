from dotenv import load_dotenv
import os
import requests

load_dotenv()

class HumeService:
    def __init__(self):
        self.HUME_API_KEY = os.getenv("HUME_API_KEY")
        self.HUME_CONFIG_ID = os.getenv("HUME_CONFIG_ID")

    def get_chat_transcript(self, chat_id : str):
            
            response = requests.get(
                f"https://api.hume.ai/v0/evi/chats/{chat_id}?page_number=0&page_size=100&ascending_order=true",
                headers={
                    "X-Hume-Api-Key": self.HUME_API_KEY
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
    
    def list_of_chats_history(self, user_id: str):
        response = requests.get(
            f"https://api.hume.ai/v0/evi/chats?page_number=0&page_size=23&ascending_order=true",
            headers={
                "X-Hume-Api-Key": self.HUME_API_KEY
            },
            )
        
        data = response.json()
        return data
    
    def get_chat_audio(self, chat_id: str):
        response = requests.get(
            f"https://api.hume.ai/v0/evi/chats/{chat_id}/audio",
            headers={
                "X-Hume-Api-Key": self.HUME_API_KEY
            },
        )

        data = response.json()
        return data