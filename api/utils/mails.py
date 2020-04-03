#!/usr/bin/env python3

from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

from app import mail, app


def send_reset_password_mail(user):
    sender = app.config['MAIL_USERNAME']
    secret_salt = app.config['SECRET_SALT']
    frontend_url = app.config['FRONTEND_URL']
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    confirm_token = serializer.dumps(user.email, salt=secret_salt)
    subject = '{} reset your password'.format(user.name)
    msg = Message(subject=subject, sender=sender, recipients=[user.email])

    msg.body = 'Hello {}\n\nwith this mail we send you the link to reset your password for your MailAPI account.\n\n{}/confirm/{}'.format(
        user.name, frontend_url, confirm_token)

    mail.send(msg)

    return True
