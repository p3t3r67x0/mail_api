#!/usr/bin/env python3

from datetime import datetime

from app import db


class SettingsModel(db.Model):
    __tablename__ = 'settings'

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
    use_ssl = db.Column(db.Boolean, default=False, nullable=False)
    use_tls = db.Column(db.Boolean, default=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime)

    def update_settings(self):
        db.session.commit()

    def create_settings(self):
        db.session.add(self)
        db.session.commit()

        return self.id
