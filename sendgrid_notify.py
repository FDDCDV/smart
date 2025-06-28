
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = "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"
FROM_EMAIL = "kontakt@77games.pl"
TO_EMAIL = "luckysteam56@gmail.com"

def send_notification_email(subject: str, message: str):
    mail = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAIL,
        subject=subject,
        plain_text_content=message
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(mail)
        print(f"Status: {response.status_code}")
        print(f"Headers: {response.headers}")
        return {"status": response.status_code, "message": "Email wysłany"}
    except Exception as e:
        print(f"SendGrid error: {e}")
        return {"error": str(e)}