#!/usr/bin/env python3

from flask import jsonify
from flask_jwt_extended.exceptions import NoAuthorizationError
from werkzeug.exceptions import NotFound, BadRequest, MethodNotAllowed, RequestEntityTooLarge, InternalServerError

from app import app


@app.errorhandler(RequestEntityTooLarge)
def handle_request_entity_too_large(e):
    return jsonify(message='Request entity too large'), 413


@app.errorhandler(NoAuthorizationError)
def handle_no_authorization_error(e):
    return jsonify(message='Missing authorization header'), 401


@app.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    return jsonify(message='Internal server error'), 500


@app.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify(message='Requested resource was not found'), 404


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify(message='Bad request please try again'), 400


@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(e):
    return jsonify(message='This method is not allowed'), 405
