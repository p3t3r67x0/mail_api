#!/usr/bin/env python3

from datetime import datetime

from flask_bcrypt import generate_password_hash, check_password_hash

from app import db
from models.settings import SettingsModel


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime)

    settings = db.relationship('SettingsModel', backref='user', lazy=True)

    def update_user(self):
        db.session.commit()

    def create_user(self):
        db.session.add(self)
        db.session.commit()

        return self.id

    @classmethod
    def find_by_email(self, email):
        return self.query.filter_by(email=email).first()

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
