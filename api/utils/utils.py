#!/usr/bin/env python3

import re
import uuid

from flask_mail import Message

from app import mail, app


def non_empty_string(s):
    if not s:
        raise ValueError('Must not be empty string')

    return s


def non_mail_address(s):
    pattern = re.compile(
        r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$')

    if not s:
        raise ValueError('Must not be empty string')

    if not pattern.match(s):
        raise ValueError('Must not be an invalid mail')

    return s


def create_id():
    return str(uuid.uuid4()).split('-')[4]


def send_mail(data):
    recipient = app.config['MAIL_RECIPIENT']
    subject = '{} {} has sent you a mail'.format(
        data.first_name, data.last_name)
    msg = Message(subject=subject, sender=data.email, recipients=[recipient])
    msg.body = data.message
    mail.send(msg)

    return data
