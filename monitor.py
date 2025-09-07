import os
import time
import schedule
from typing import Set
from models import db, User
from email_service import EmailService
from data_service import DatabaseService
from tgtg_service import TgtgService
from app import create_app


class TgtgMonitor:
    def __init__(self, server_url: str = "http://localhost:5001"):
        self.email_service = EmailService(os.getenv('SENDINBLUE_API_KEY'))
        self.data_service = DatabaseService()
        self.tgtg_service = TgtgService()
        self.server_url = server_url

    def check_favorites(self):
        """Check favorites for all active users"""
        active_users = self.data_service.get_active_users()
        print(f"🔍 Checking {len(active_users)} active users...")

        for user in active_users:
            self._check_user_favorites(user)

    def _check_user_favorites(self, user: User):
        """Check favorites for a single user"""
        try:
            print(f"\n👤 Checking {user.email}...")

            # Get user credentials
            credentials = self.data_service.get_user_credentials(user)
            if not credentials:
                print(f"❌ No credentials found for {user.email}")
                return

            # Create authenticated client
            client = self.tgtg_service.create_client(credentials)

            # Get current items
            current_items = client.get_items()
            print(
                f"📱 Retrieved {len(current_items)} total items from TGTG API")

            # Process current available items to get store set
            current_available_stores = []
            current_store_names = set()

            for item in current_items:
                available = item.get('items_available', 0)
                if available > 0:
                    item_key = self.tgtg_service.get_item_key(item)
                    store_name = item['store']['store_name']
                    item_name = item['item']['name']
                    price = item['item']['item_price']['minor_units'] / 100
                    address = item['pickup_location']['address']['address_line']

                    item_data = {
                        'store': store_name,
                        'item': item_name,
                        'available': available,
                        'price': price,
                        'address': address,
                        'key': item_key,
                        'is_new': False  # We'll determine this below
                    }

                    current_available_stores.append(item_data)
                    current_store_names.add(store_name)

            print(
                f"🏪 Found {len(current_available_stores)} stores with available items")

            # Get stores from last email sent
            last_emailed_stores = self.data_service.get_last_emailed_stores(
                user)
            print(
                f"📧 Last email contained stores: {sorted(last_emailed_stores)}")

            # Only send email if there are NEW stores added (not removed)
            stores_added = current_store_names - last_emailed_stores
            should_send_email = len(stores_added) > 0 and len(
                current_available_stores) > 0

            print(f"🆕 New stores detected: {sorted(stores_added)}")
            print(f"📬 Should send email: {should_send_email}")

            if should_send_email:
                # Mark new stores (stores not in last email)
                for item_data in current_available_stores:
                    if item_data['store'] in stores_added:
                        item_data['is_new'] = True

                new_stores_count = len(stores_added)

                print(f"📧 New stores detected for {user.email}")
                print(f"   Last email stores: {sorted(last_emailed_stores)}")
                print(f"   Current stores: {sorted(current_store_names)}")
                print(f"   New stores added: {sorted(stores_added)}")

                # Send notification - FIXED: Added missing closing parenthesis
                success = self.email_service.send_notification(
                    user.email,
                    current_available_stores,
                    new_stores_count,
                    self.server_url
                )  # <-- FIXED: This closing parenthesis was missing!

                if success:
                    # Record this email in database
                    self.data_service.record_email_sent(
                        user, current_available_stores)

                    print(
                        f"✅ Email sent to {user.email} with {len(current_available_stores)} stores")
                    for item in current_available_stores:
                        status = "NEW!" if item['is_new'] else "existing"
                        print(
                            f"   🏪 {item['store']} ({status}) - {item['available']} bags")
                else:
                    print(f"❌ Failed to send email to {user.email}")

            else:
                if current_available_stores:
                    stores_removed = last_emailed_stores - current_store_names
                    if stores_removed:
                        print(
                            f"📋 Store(s) sold out for {user.email}: {sorted(stores_removed)} - no email sent")
                    else:
                        print(
                            f"📋 No new stores for {user.email} - {len(current_available_stores)} stores still available")
                    print(f"   Current stores: {sorted(current_store_names)}")
                else:
                    print(f"📭 No bags available for {user.email}")

        except Exception as e:
            print(f"❌ Error checking favorites for {user.email}: {e}")
            import traceback
            traceback.print_exc()

    def start(self, check_interval_minutes: int = 5):
        """Start the monitoring service"""
        print("🚀 Starting TooGoodToGo monitor with store-addition tracking...")
        print("📧 Sending emails ONLY when NEW stores are added to your favorites")
        print("🏪 Store removals and quantity changes = no emails")
        print("✨ Store reintroductions = new emails")
        print(f"⏰ Checking every minute")

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
    SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:5001')
    monitor = TgtgMonitor(SERVER_URL)
    monitor.start()


if __name__ == "__main__":
    main()
