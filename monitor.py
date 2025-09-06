import time
import schedule
from typing import Set
from models import db, User
from email_service import EmailService
from data_service import DatabaseService
from tgtg_service import TgtgService
from app import create_app


class TgtgMonitor:
    def __init__(self, server_url: str = "http://localhost:5000"):
        self.email_service = EmailService()
        self.data_service = DatabaseService()
        self.tgtg_service = TgtgService()
        self.server_url = server_url

    def check_favorites(self):
        """Check favorites for all active users"""
        active_users = self.data_service.get_active_users()

        for user in active_users:
            self._check_user_favorites(user)

    def _check_user_favorites(self, user: User):
        """Check favorites for a single user"""
        try:
            # Get user credentials
            credentials = self.data_service.get_user_credentials(user)
            if not credentials:
                print(f"❌ No credentials found for {user.email}")
                return

            # Create authenticated client
            client = self.tgtg_service.create_client(credentials)

            # Get current items and previously notified items
            current_items = client.get_items()
            previously_notified = self.data_service.get_previously_notified_items(
                user)

            # Process items to find new ones
            all_available, new_items, _ = self.tgtg_service.process_items(
                current_items, previously_notified
            )

            # Send notification if there are new items
            if new_items:
                print(
                    f"📧 Sending notification for {len(new_items)} new items to {user.email}")

                success = self.email_service.send_notification(
                    user.email, all_available, len(new_items), self.server_url
                )

                if success:
                    # Record notifications in database
                    for item in new_items:
                        self.data_service.add_notification_record(
                            user, item['key'], item['store'], item['item']
                        )
                        print(
                            f"🆕 NEW: {item['available']} bags at '{item['store']}' - {item['item']}")
            else:
                if all_available:
                    print(
                        f"📋 {len(all_available)} bags available but no new items for {user.email}")
                else:
                    print(f"📭 No bags available for {user.email}")

        except Exception as e:
            print(f"❌ Error checking favorites for {user.email}: {e}")

    def start(self, check_interval_minutes: int = 15):
        """Start the monitoring service"""
        print("🚀 Starting TooGoodToGo monitor with database backend...")
        print("🆕 Sending notifications only when NEW items become available")
        print("📧 Beautiful terminal-themed emails with unsubscribe functionality")
        print(f"⏰ Checking every {check_interval_minutes} minutes")

        # Create Flask app context for database operations
        app = create_app()
        with app.app_context():
            print("\n🔍 Running initial check...")
            self.check_favorites()

            schedule.every(check_interval_minutes).minutes.do(
                lambda: self._run_with_app_context(app)
            )

            print("\n✅ Monitor started successfully!")
            print("Press Ctrl+C to stop the monitor\n")

            try:
                while True:
                    schedule.run_pending()
                    time.sleep(60)
            except KeyboardInterrupt:
                print("\n👋 Monitor stopped by user")

    def _run_with_app_context(self, app):
        """Run check_favorites within Flask app context"""
        with app.app_context():
            self.check_favorites()


def main():
    SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:5000')

    monitor = TgtgMonitor(SERVER_URL)
    monitor.start()


if __name__ == "__main__":
    main()
