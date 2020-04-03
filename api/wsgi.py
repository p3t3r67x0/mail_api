#!/usr/bin/env python3

from app import app, db, jwt, api

import resources.resources as resources
import errors.errors as errors

@app.before_first_request
def create_tables():
    db.create_all()


@jwt.token_in_blacklist_loader
def check_token_blacklisted(decrypted_token):
    jti = decrypted_token['jti']


@jwt.revoked_token_loader
def custom_revoked_token():
    return jsonify(message='Token has been revoked'), 401


@jwt.unauthorized_loader
def custom_unauthorized(self):
    return jsonify(message=self), 401


@jwt.invalid_token_loader
def custom_invalid_token(self):
    return jsonify(message=self), 422


@jwt.expired_token_loader
def custom_expired_token(expired_token):
    token_type = expired_token['type']

    return jsonify({
        'message': 'The {} token has expired'.format(token_type)
    }), 401


api.add_resource(resources.MailEndpoint, '/mail')
api.add_resource(resources.LoginEndpoint, '/login')
api.add_resource(resources.SignupEndpoint, '/signup')
api.add_resource(resources.ResetPasswordEndpoint, '/reset')
api.add_resource(resources.ChangePasswordEndpoint, '/change')
api.add_resource(resources.ConfirmTokenEndpoint, '/confirm')
api.add_resource(resources.TokenRefreshEndpoint, '/token/refresh')
api.add_resource(resources.SettingsByUserIdEnpoint, '/settings/u/<user_id>')
api.add_resource(resources.SettingsByIdEnpoint, '/settings/i/<id>')


if __name__ == '__main__':
    app.run(debug=True)
