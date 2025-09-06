from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
from datetime import datetime
import json
import os

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255))
    monitoring_enabled = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    credentials = db.relationship(
        'UserCredentials', backref='user', uselist=False, cascade='all, delete-orphan')
    notifications = db.relationship(
        'NotificationHistory', backref='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserCredentials(db.Model):
    __tablename__ = 'user_credentials'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    encrypted_credentials = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_credentials(self, credentials_dict):
        """Encrypt and store TooGoodToGo credentials"""
        key = self._get_encryption_key()
        cipher = Fernet(key)
        credentials_json = json.dumps(credentials_dict)
        self.encrypted_credentials = cipher.encrypt(
            credentials_json.encode()).decode()

    def get_credentials(self):
        """Decrypt and return TooGoodToGo credentials"""
        key = self._get_encryption_key()
        cipher = Fernet(key)
        decrypted_bytes = cipher.decrypt(self.encrypted_credentials.encode())
        return json.loads(decrypted_bytes.decode())

    def _get_encryption_key(self):
        """Get or generate encryption key"""
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            # Generate a key if not exists (store this securely!)
            key = Fernet.generate_key().decode()
            # In production, store this in a secure key management service
        return key.encode()


class NotificationHistory(db.Model):
    __tablename__ = 'notification_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_key = db.Column(db.String(255), nullable=False, index=True)
    store_name = db.Column(db.String(255), nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    notified_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Composite index for efficient queries
    __table_args__ = (
        db.Index('idx_user_item_notified', 'user_id',
                 'item_key', 'notified_at'),
    )
