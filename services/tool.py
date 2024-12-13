import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def book_meeting(email: str) -> str:
    '''
    This tool is used to send a meeting booking link to the provided email.

    Args:
        email: Email adress of the user
    '''
    meeting_link = os.getenv("MEETING_LINK")
    subject = "Your Meeting Booking Link"
    body = f"Hello,\n\nPlease use the following link to book your meeting:\n{meeting_link}\n\nBest regards,\nYour Company"

    sender_email = os.getenv("EMAIL_ID")
    sender_password = os.getenv("EMAIL_PASSWORD")

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
        server.close()
        return f"Meeting link has been sent to {email}"
    except Exception as e:
        return f"Failed to send email. Error: {str(e)}"
