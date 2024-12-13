from pydantic import BaseModel

class TwilioCredentials(BaseModel):
    account_sid: str
    auth_token: str

class TwilioAndPhoneCredentials(BaseModel):
    account_sid: str
    auth_token: str
    phone_number: str