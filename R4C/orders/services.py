import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(customer_email, model, version):
    sender = os.getenv("EMAIL_LOGIN")
    password = os.getenv("EMAIL_PASSWORD")

    subjects = "Дорогой покупатель!"
    message = ("Добрый день!\n"
               f"Недавно вы интересовались нашим роботом модели {model}, версии {version}.\n"
               "Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами\n")
    mime = MIMEText(message, "utf-8")
    mime["Subject"] = Header(subjects, "utf-8")

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, customer_email, mime.as_string())
