from fastapi import HTTPException
from dotenv import load_dotenv
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from models.phone import TwilioCredentials, TwilioAndPhoneCredentials

load_dotenv()

class PhoneService:
    def __init__(self):
        self.TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
        self.TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

    def check_twilio_account(self, credentials: TwilioCredentials):
        try:
            client = Client(credentials.account_sid, credentials.auth_token)
            account = client.api.accounts(credentials.account_sid).fetch()
            
            return client
            
        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid Twilio credentials. Please check your Account SID and Auth Token. Error: {str(e)}"
            )
        
    
    def phone_status(self, phone_number: str):
        try:
            client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)
            
            incoming_numbers = client.incoming_phone_numbers.list(phone_number=phone_number)
            
            found_number = None
            for number in incoming_numbers:
                if number.phone_number == phone_number:
                    found_number = number
                    break
            
            if not found_number:
                return None
                
            number_details = {
                "friendly_name": found_number.friendly_name,
                "phone_number": found_number.phone_number,
                "sid": found_number.sid,
                "capabilities": {
                    "voice": found_number.capabilities.get('voice', False),
                    "SMS": found_number.capabilities.get('sms', False),
                    "MMS": found_number.capabilities.get('mms', False),
                    "fax": found_number.capabilities.get('fax', False)
                },
                "status": "in-use",
                "voice_url": found_number.voice_url,
                "sms_url": found_number.sms_url,
                "voice_method": found_number.voice_method,
                "sms_method": found_number.sms_method
            }
            
            return number_details

        except TwilioRestException as e:
            print(f"Twilio error: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None
    
    

    def list_phone_numbers(self, credentials: TwilioCredentials):
        try:
            client = self.check_twilio_account(credentials)
            
            incoming_numbers = client.incoming_phone_numbers.list()
            
            owned_numbers = [{
                "friendly_name": number.friendly_name,
                "phone_number": number.phone_number,
                "sid": number.sid,
                "capabilities": {
                    "voice": number.capabilities.get('voice', False),
                    "SMS": number.capabilities.get('sms', False),
                    "MMS": number.capabilities.get('mms', False),
                    "fax": number.capabilities.get('fax', False)
                },
                "status": number.status,
                "voice_url": number.voice_url,
                "sms_url": number.sms_url,
                "voice_method": number.voice_method,
                "sms_method": number.sms_method
            } for number in incoming_numbers]
            
            return owned_numbers
            
        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Error fetching owned phone numbers: {str(e)}"
            )
        
    async def phone_service_integration(self, credentials: TwilioAndPhoneCredentials):
        try:
            client = self.check_twilio_account(credentials)

            if not self.verify_phone_number(client, credentials.phone_number):
                raise HTTPException(
                    status_code=400,
                    detail="The provided phone number is not owned by this Twilio account"
                )

            try:
                phone_number = client.incoming_phone_numbers.list(
                    phone_number=credentials.phone_number
                )[0]

                phone_number.update(
                    voice_url="YOUR_WEBHOOK_URL",
                    voice_method="POST",
                    status_callback="YOUR_STATUS_CALLBACK_URL",
                    status_callback_method="POST"
                )
            except IndexError:
                raise HTTPException(
                    status_code=404,
                    detail="Phone number not found in Twilio account"
                )

            config_data = {
                "account_sid": credentials.account_sid,
                "auth_token": credentials.auth_token,
                "phone_number": credentials.phone_number,
                "voice_enabled": True,
                "created_at": "NOW()"
            }
            
            # Example Supabase insert (modify according to your setup)
            # result = await self.supabase.table("twilio_config").insert(config_data).execute()

            return {
                "status": "success",
                "message": "Phone service configuration updated successfully",
                "phone_number": credentials.phone_number
            }

        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=400,
                detail=f"Error updating phone number voice configuration: {str(e)}"
            )
        

    def verify_phone_number(self, client: Client, phone_number: str) -> bool:
        try:
            incoming_phone_numbers = client.incoming_phone_numbers.list()
            return any(number.phone_number == phone_number for number in incoming_phone_numbers)
        except TwilioRestException:
            return False