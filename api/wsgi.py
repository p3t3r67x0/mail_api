#!/usr/bin/env python3

import re
import json
import uuid

from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

from flask import Flask, jsonify, request
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_restful import Resource, Api, fields, reqparse, inputs
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash


app = Flask(__name__, static_folder=None)

app.config.from_pyfile('.config')
bcrypt = Bcrypt(app)
mail = Mail(app)
jwt = JWTManager(app)
api = Api(app, prefix='/api/v1', catch_all_404s=True)
db = SQLAlchemy(app)


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


class Settings(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey(
        'user.id'), nullable=False)
    recipient = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    smtp_port = db.Column(db.String(80), nullable=False)
    smtp_server = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    secret = db.Column(db.String(240), nullable=False)
    use_ssl = db.Column(db.Boolean, nullable=False)
    use_tls = db.Column(db.Boolean, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime)


class User(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime)

    settings = db.relationship('Settings', backref='user', lazy=True)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


def send_mail(data):
    recipient = app.config['MAIL_RECIPIENT']
    subject = '{} {} has sent you a mail'.format(
        data.first_name, data.last_name)
    msg = Message(subject=subject, sender=data.email, recipients=[recipient])
    msg.body = data.message
    mail.send(msg)

    return data


class SignupEndpoint(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)

        self.reqparse.add_argument(
            'email', type=non_mail_address, required=True, help='No valid email provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'password', type=non_empty_string, required=True, help='No message body provided', location='json', nullable=False)

        super(SignupEndpoint, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()

        user = User(**args)
        user.id = create_id()
        user.hash_password()

        try:
            db.session.add(user)
            db.session.commit()

            return {'message': 'You signed up successfully, please check your mail'}
        except IntegrityError as e:
            return {'message': 'User with given email address already exists'}, 409


class LoginEndpoint(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)

        self.reqparse.add_argument(
            'email', type=non_mail_address, required=True, help='No valid email provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'password', type=non_empty_string, required=True, help='No message body provided', location='json', nullable=False)

        super(LoginEndpoint, self).__init__()

    @jwt_required
    def get(self):
        return {'message': 'You are logged in as {}'.format(get_jwt_identity())}

    def post(self):
        args = self.reqparse.parse_args()

        try:
            user = User.query.filter_by(email=args.email).first()
            authorized = user.check_password(args.password)

            if not authorized:
                return {'message': 'Error invalid email or password'}, 401

            access_token = create_access_token(
                identity=user.email, expires_delta=timedelta(days=7))

            return {'token': access_token, 'message': 'You are successfully loged in'}
        except Exception as e:
            raise e
            return {'message': 'Error invalid email or password'}, 401


class SettingsByIdEnpoint(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)

        self.reqparse.add_argument(
            'recipient', type=non_mail_address, required=True, help='No valid email provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'username', type=non_empty_string, required=True, help='No username provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'first_name', type=non_empty_string, required=True, help='No first name provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'last_name', type=non_empty_string, required=True, help='No last name provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'secret', type=non_empty_string, required=True, help='No secret provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'password', type=non_empty_string, required=True, help='No password provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'smtp_port', type=non_empty_string, required=True, help='No smtp port provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'smtp_server', type=non_empty_string, required=True, help='No smtp server provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'use_ssl', type=inputs.boolean, required=True, help='No flag ssl provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'use_tls', type=inputs.boolean, required=True, help='No flag tls provided', location='json', nullable=False)

        super(SettingsByIdEnpoint, self).__init__()

    def get(self, id):
        settings = Settings.query.filter_by(id=id).first()

        if not settings:
            return {'message': 'Requested resource was not found'}, 404

        return {'recipient': settings.recipient,
                'first_name': settings.first_name,
                'last_name': settings.last_name,
                'smtp_port': settings.smtp_port,
                'smtp_server': settings.smtp_server,
                'password': settings.password,
                'username': settings.username,
                'secret': settings.secret,
                'use_ssl': settings.use_ssl,
                'use_tls': settings.use_tls}

    def delete(self, id):
        settings = Settings.query.filter_by(id=id).first()

        if not settings:
            return {'message': 'Requested resource settings was not found'}

        db.session.delete(settings)
        db.session.commit()

        return {'message': 'Successfully deleted resource settings'}

    def put(self, id):
        args = self.reqparse.parse_args()

        try:
            settings = Settings.query.filter_by(id=id).first()

            if not settings:
                return {'message': 'Requested resource was not found'}, 404

            settings.recipient = args.recipient
            settings.first_name = args.first_name
            settings.last_name = args.last_name
            settings.smtp_port = args.smtp_port
            settings.smtp_server = args.smtp_server
            settings.password = args.password
            settings.username = args.username
            settings.secret = args.secret
            settings.use_ssl = args.use_ssl
            settings.use_tls = args.use_tls
            settings.updated = datetime.utcnow()

            db.session.commit()

            return {'message': 'Successfully updated resource settings'}
        except Exception as e:
            raise


class SettingsByUserIdEnpoint(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)

        self.reqparse.add_argument(
            'recipient', type=non_mail_address, required=True, help='No valid email provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'username', type=non_empty_string, required=True, help='No username provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'first_name', type=non_empty_string, required=True, help='No first name provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'last_name', type=non_empty_string, required=True, help='No last name provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'secret', type=non_empty_string, required=True, help='No secret provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'password', type=non_empty_string, required=True, help='No password provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'smtp_port', type=non_empty_string, required=True, help='No smtp port provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'smtp_server', type=non_empty_string, required=True, help='No smtp server provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'use_ssl', type=inputs.boolean, required=True, help='No flag ssl provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'use_tls', type=inputs.boolean, required=True, help='No flag tls provided', location='json', nullable=False)

        super(SettingsByUserIdEnpoint, self).__init__()

    def get(self, user_id):
        settings = Settings.query.filter_by(user_id=user_id).all()
        results = []

        if not settings:
            return {'message': 'Requested resource was not found'}, 404

        for item in settings:
            results.append({'id': item.id,
                            'user_id': item.user_id,
                            'recipient': item.recipient,
                            'first_name': item.first_name,
                            'last_name': item.last_name,
                            'smtp_port': item.smtp_port,
                            'smtp_server': item.smtp_server,
                            'password': item.password,
                            'username': item.username,
                            'secret': item.secret,
                            'use_ssl': item.use_ssl,
                            'use_tls': item.use_tls})

        return results

    def post(self, user_id):
        args = self.reqparse.parse_args()

        settings = Settings(**args)
        settings.id = create_id()
        settings.user_id = user_id

        try:
            db.session.add(settings)
            db.session.commit()

            return {'message': 'Successfully created resource settings'}
        except IntegrityError as e:
            return {'message': e.args}


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

        return {'message': 'Your mail was sent successfully'}


api.add_resource(MailEnpoint, '/mail')
api.add_resource(LoginEndpoint, '/login')
api.add_resource(SignupEndpoint, '/signup')
api.add_resource(SettingsByUserIdEnpoint, '/settings/u/<user_id>')
api.add_resource(SettingsByIdEnpoint, '/settings/i/<id>')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
