from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from enhanced_email_sender import send_email

router = APIRouter()

# Test endpoint (GET)
@router.get("/send-test-email")
def send_test_email():
    test_recipient = "yourname@gmail.com"  # Replace with your test email
    subject = "Ky’ra Email Test – SendGrid Integration Success"
    html_content = """
    <h2>Shalom from Ky’ra!</h2>
    <p>This is a test email confirming successful SendGrid setup with <strong>notifications@kyras.in</strong>.</p>
    <p>God bless you abundantly! 💚</p>
    """
    try:
        send_email([test_recipient], subject, html_content)
        return {"status": "✅ Email sent successfully", "to": test_recipient}
    except Exception as e:
        return {"status": "❌ Failed to send email", "error": str(e)}

# Dynamic email endpoint (POST)
class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    html_content: str

@router.post("/send-email")
def send_custom_email(request: EmailRequest):
    try:
        send_email([request.to_email], request.subject, request.html_content)
        return {
            "status": "✅ Email sent successfully",
            "to": request.to_email
        }
    except Exception as e:
        return {
            "status": "❌ Failed to send email",
            "error": str(e)
        }