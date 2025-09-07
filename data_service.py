from models import db, User, UserCredentials, NotificationHistory
from flask_login import current_user
from datetime import datetime
from typing import List, Dict, Optional, Set


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

    def get_last_emailed_stores(self, user: User) -> Set[str]:
        """Get set of store names from the most recent email sent to user"""
        # Get the most recent notification timestamp for this user
        latest_notification = NotificationHistory.query.filter_by(
            user_id=user.id
        ).order_by(NotificationHistory.notified_at.desc()).first()

        if not latest_notification:
            return set()  # No previous emails sent

        # Get all notifications from that same timestamp (same email batch)
        latest_timestamp = latest_notification.notified_at
        notifications_from_last_email = NotificationHistory.query.filter_by(
            user_id=user.id,
            notified_at=latest_timestamp
        ).all()

        # Return set of store names from that email
        return set(notif.store_name for notif in notifications_from_last_email)

    def record_email_sent(self, user: User, available_stores: List[Dict]):
        """Record that an email was sent with these stores"""
        timestamp = datetime.utcnow()

        # Create notification records for all stores in this email
        for store_data in available_stores:
            notification = NotificationHistory(
                user=user,
                item_key=store_data['key'],
                store_name=store_data['store'],
                item_name=store_data['item'],
                notified_at=timestamp  # Same timestamp for all items in this email
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
