# phone.py

from fastapi import APIRouter, HTTPException, Path
from twilio.rest import Client
from pydantic import BaseModel
from typing import Optional

from models.phone import TwilioCredentials, TwilioAndPhoneCredentials
from services.phone import PhoneService

router = APIRouter()
phone_service = PhoneService()

class UserData(BaseModel):
    name: str
    email: str
    company: str
    description: Optional[str] = ""
    phone_number: str


@router.get("/phone/list_numbers")
async def add_twilio_credentials(credentials: TwilioCredentials):
    if not credentials:
        return None
    
    list_of_owned_numbers = phone_service.list_phone_numbers(credentials)
    return list_of_owned_numbers


@router.post("/phone/integration/{user_id}")
async def phone_service_integration(credentials: TwilioAndPhoneCredentials):
    if not credentials:
        return None
    
    return phone_service.phone_service_integration(credentials)


@router.get("/phone/status/{phone_number}")
def check_phone_number_status(phone_number : str = Path(...)):
    if not phone_number:
        return None
    
    return phone_service.phone_status(phone_number)
