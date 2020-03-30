#!/usr/bin/env python3

import re
import json

from flask import Flask, jsonify, request
from flask_mail import Mail, Message
from flask_restful import Resource, Api, fields, reqparse, marshal_with


app = Flask(__name__, static_folder=None)

app.config.from_pyfile('.config')

mail = Mail(app)
api = Api(app, prefix='/api/v1', catch_all_404s=True)


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


def send_mail(data):
    recipient = app.config['MAIL_RECIPIENT']
    subject = '{} {} has sent you a mail'.format(
        data.first_name, data.last_name)
    msg = Message(subject=subject, sender=data.email, recipients=[recipient])
    msg.body = data.message
    mail.send(msg)

    return data


class MailEnpoint(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument(
            'email', type=non_mail_address, required=True, help='No valid email provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'message', type=non_empty_string, required=True, help='No message body provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'first_name', type=non_empty_string, required=True, help='No first name provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'last_name', type=non_empty_string, required=True, help='No last name provided', location='json', nullable=False)

        super(MailEnpoint, self).__init__()

    def post(self):
        send_mail(self.reqparse.parse_args())
        message = {'message': 'Your mail was sent successfully'}

        return jsonify(message)


api.add_resource(MailEnpoint, '/mail')


if __name__ == '__main__':
    app.run(debug=True)
