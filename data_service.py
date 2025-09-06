from models import db, User, UserCredentials, NotificationHistory
from flask_login import current_user
from datetime import datetime
from typing import List, Dict, Optional


class DatabaseService:
    def __init__(self):
        pass

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return User.query.filter_by(email=email).first()

    def create_user(self, email: str, tgtg_credentials: dict) -> User:
        """Create new user with encrypted credentials"""
        user = User(email=email)

        # Store encrypted credentials
        credentials = UserCredentials(user=user)
        credentials.set_credentials(tgtg_credentials)

        db.session.add(user)
        db.session.add(credentials)
        db.session.commit()

        return user

    def get_active_users(self) -> List[User]:
        """Get all users with monitoring enabled and credentials"""
        return User.query.filter_by(monitoring_enabled=True)\
            .join(UserCredentials)\
            .all()

    def get_user_credentials(self, user: User) -> dict:
        """Get decrypted TooGoodToGo credentials for user"""
        if user.credentials:
            return user.credentials.get_credentials()
        return {}

    def get_previously_notified_items(self, user: User) -> set:
        """Get set of item keys previously notified to user"""
        notifications = NotificationHistory.query.filter_by(
            user_id=user.id).all()
        return set(notif.item_key for notif in notifications)

    def add_notification_record(self, user: User, item_key: str, store_name: str, item_name: str):
        """Record that user was notified about an item"""
        notification = NotificationHistory(
            user=user,
            item_key=item_key,
            store_name=store_name,
            item_name=item_name
        )
        db.session.add(notification)
        db.session.commit()

    def remove_user(self, email: str) -> bool:
        """Remove user and all associated data"""
        user = self.get_user_by_email(email)
        if user:
            # Cascade will delete credentials and notifications
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    def disable_monitoring(self, user: User):
        """Disable monitoring for user"""
        user.monitoring_enabled = False
        db.session.commit()

    def enable_monitoring(self, user: User):
        """Enable monitoring for user"""
        user.monitoring_enabled = True
        db.session.commit()
