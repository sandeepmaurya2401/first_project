import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
import random


load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(to_email: str, otp: str):
    msg = EmailMessage()
    msg["Subject"] = "Your OTP Code"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg.set_content(f"Your OTP is: {otp}\nValid for 5 minutes.")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        smtp.send_message(msg)
