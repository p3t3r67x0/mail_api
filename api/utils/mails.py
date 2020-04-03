#!/usr/bin/env python3

from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

from app import mail, app


sender = app.config['MAIL_USERNAME']
secret_salt = app.config['SECRET_SALT']
frontend_url = app.config['FRONTEND_URL']
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


def send_reset_password_mail(user):
    confirm_token = serializer.dumps(user.email, salt=secret_salt)
    subject = '{} reset your password'.format(user.name)
    msg = Message(subject=subject, sender=sender, recipients=[user.email])

    msg.body = 'Hello {},\n\nwith this mail we send you the link to reset your password for your MailAPI account.\n\n{}/change/{}\n\nBest regards\nMailAPI Team'.format(
        user.name, frontend_url, confirm_token)

    mail.send(msg)

    return True


def send_confirm_mail(user):
    confirm_token = serializer.dumps(user.email, salt=secret_salt)
    subject = '{} confirm your account'.format(user.name)
    msg = Message(subject=subject, sender=sender, recipients=[user.email])

    msg.body = 'Hello {},\n\nwith this mail we send you the confirmation link for your MailAPI account.\n\n{}/confirm/{}\n\nBest regards\nMailAPI Team'.format(
        user.name, frontend_url, confirm_token)

    mail.send(msg)

    return True
