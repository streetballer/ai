import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src.common.environment.config import SMTP_FROM, SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USER


def send_email(to: str, subject: str, body_html: str) -> None:
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = SMTP_FROM
    message["To"] = to
    message.attach(MIMEText(body_html, "html"))
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASSWORD)
            smtp.sendmail(SMTP_FROM, to, message.as_string())
    except Exception:
        pass
