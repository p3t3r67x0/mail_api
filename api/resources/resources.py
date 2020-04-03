#!/usr/bin/env python3

from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

from flask import jsonify, request, g
from flask_restful import Resource, reqparse, inputs
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, decode_token, get_raw_jwt
from itsdangerous import URLSafeTimedSerializer, BadSignature, BadTimeSignature, SignatureExpired

from models.users import UserModel
from models.settings import SettingsModel
from utils.utils import non_empty_string, non_mail_address, create_id, send_mail
from utils.mails import send_reset_password_mail
from app import app, db


serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


class TokenRefreshEndpoint(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        expires = timedelta(days=7)
        access_token = create_access_token(
            identity=current_user, expires_delta=expires)

        return {'access_token': access_token}


class SignupEndpoint(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)

        self.reqparse.add_argument(
            'name', type=non_empty_string, required=True, help='No valid name provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'email', type=non_mail_address, required=True, help='No valid email provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'password', type=non_empty_string, required=True, help='No message body provided', location='json', nullable=False)

        super(SignupEndpoint, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()

        user = UserModel(**args)
        user.id = create_id()
        user.hash_password()

        try:
            user.create_user()

            return {'message': 'Please check your inbox'}
        except IntegrityError as e:
            return {'message': 'Email address already exists'}, 409


class LoginEndpoint(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)

        self.reqparse.add_argument(
            'email', type=non_mail_address, required=True, help='No valid email provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'password', type=non_empty_string, required=True, help='No valid password provided', location='json', nullable=False)

        super(LoginEndpoint, self).__init__()

    @jwt_required
    def get(self):
        return {'message': 'You are logged in as {}'.format(get_jwt_identity())}

    def post(self):
        args = self.reqparse.parse_args()

        try:
            user = UserModel.find_by_email(args.email)

            if not user:
                return {'message': 'Error invalid email or password'}, 401

            authorized = user.check_password(args.password)

            if not authorized:
                return {'message': 'Error invalid email or password'}, 401

            access_token = create_access_token(
                identity=user.email, expires_delta=timedelta(days=7))
            refresh_token = create_refresh_token(identity=user.email)

            return {'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user_id': user.id}
        except Exception as e:
            raise e
            return {'message': 'Error invalid email or password'}, 401


class ResetPasswordEndpoint(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)

        self.reqparse.add_argument(
            'email', type=non_mail_address, required=True, help='No valid email provided', location='json', nullable=False)

        super(ResetPasswordEndpoint, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()

        try:
            user = UserModel.find_by_email(args.email)

            if not user:
                return {'message': 'Email address was not found'}, 404

            result = send_reset_password_mail(user)

            if not result:
                return {'message': 'Error please try again'}, 500

            return {'message': 'Please check your inbox'}
        except Exception as e:
            raise


class ChangePasswordEndpoint(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)

        self.reqparse.add_argument(
            'password', type=non_empty_string, required=True, help='No valid password provided', location='json', nullable=False)
        self.reqparse.add_argument(
            'token', type=non_empty_string, required=True, help='No valid token provided', location='json', nullable=False)

        super(ChangePasswordEndpoint, self).__init__()

    def put(self):
        args = self.reqparse.parse_args()
        salt = app.config['SECRET_SALT']

        try:
            email = serializer.loads(args.token, salt=salt, max_age=7200)
        except SignatureExpired as e:
            return {'message': 'Token expired try forgot password'}, 401
        except BadTimeSignature as e:
            return {'message': 'Unknown error try forgot password'}, 400
        except BadSignature as e:
            return {'message': 'Invalid token try forgot password'}, 422

        try:
            user = UserModel.find_by_email(email)

            if not user:
                return {'message': 'Email address was not found'}, 404

            user.password = args.password
            user.hash_password()
            user.update_user()

            return {'message': 'Successfully updated password'}
        except Exception as e:
            raise


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

    @jwt_required
    def get(self, id):
        settings = SettingsModel.query.filter_by(id=id).first()

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

    @jwt_required
    def delete(self, id):
        settings = SettingsModel.query.filter_by(id=id).first()

        if not settings:
            return {'message': 'Requested resource settings was not found'}

        db.session.delete(settings)
        db.session.commit()

        return {'message': 'Successfully deleted resource settings'}

    @jwt_required
    def put(self, id):
        args = self.reqparse.parse_args()

        try:
            settings = SettingsModel.query.filter_by(id=id).first()

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
    @jwt_required
    def get(self, user_id):
        settings = SettingsModel.query.filter_by(user_id=user_id).all()
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

    @jwt_required
    def post(self, user_id):
        settings = SettingsModel()

        settings.id = create_id()
        settings.user_id = user_id
        settings.recipient = ''
        settings.first_name = ''
        settings.last_name = ''
        settings.smtp_port = ''
        settings.smtp_server = ''
        settings.password = ''
        settings.username = ''
        settings.secret = ''

        try:
            db.session.add(settings)
            db.session.commit()

            return {'message': 'Successfully created resource settings', 'id': settings.id}
        except IntegrityError as e:
            return {'message': e.args}


class MailEndpoint(Resource):
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

        super(MailEndpoint, self).__init__()

    def post(self):
        send_mail(self.reqparse.parse_args())

        return {'message': 'Your mail was sent successfully'}
