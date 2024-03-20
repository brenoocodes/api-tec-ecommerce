from fastapi import BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from itsdangerous import URLSafeSerializer
from src.configure import app, SECRET_KEY
import os

serializer = URLSafeSerializer(SECRET_KEY)

conf = ConnectionConfig(
    MAIL_USERNAME="your_email",
    MAIL_PASSWORD="your_password",
    MAIL_FROM="your_email",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

class EmailSchema(BaseModel):
    email: str
    subject: str
    link: str

def send_email(email: str, subject: str, link: str, html_template: str):
    fm = FastMail(conf)
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=html_template.format(link),
        subtype="html"
    )
    fm.send_message(message)

def read_html_template(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

@app.post("/send-email/")
async def send_email_endpoint(email_data: EmailSchema):
    html_template_path = os.path.join("templates", "confirmar.html")
    html_template = read_html_template(html_template_path)

    task = BackgroundTasks()
    task.add_task(send_email, email_data.email, email_data.subject, email_data.link, html_template)
    return {"message": "Email being sent"}

