from flask_mail import Message
from app import mail

def send_update_email(to_email, subject, body):
    msg = Message(subject, recipients=[to_email])
    msg.body = body
    mail.send(msg)
