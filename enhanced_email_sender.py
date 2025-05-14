import os
import base64
from typing import List, Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
DEFAULT_SENDER_EMAIL = 'notifications@kyras.in'

def send_email(
    to_emails: List[str],
    subject: str,
    html_content: str,
    attachments: Optional[List[dict]] = None
):
    if not SENDGRID_API_KEY:
        raise ValueError("SendGrid API key not found in environment variables.")
    
    message = Mail(
        from_email=DEFAULT_SENDER_EMAIL,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content
    )

    # Attach files if provided
    if attachments:
        for file in attachments:
            with open(file['path'], 'rb') as f:
                data = f.read()
                encoded = base64.b64encode(data).decode()
                attachedFile = Attachment(
                    FileContent(encoded),
                    FileName(file['filename']),
                    FileType(file['type']),
                    Disposition('attachment')
                )
                message.add_attachment(attachedFile)

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"✅ Email sent to {to_emails}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        raise