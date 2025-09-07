from sib_api_v3_sdk import ApiClient, Configuration, TransactionalEmailsApi, SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException
import urllib.parse


class EmailService:
    def __init__(self, api_key):
        configuration = Configuration()
        configuration.api_key['api-key'] = api_key
        self.api_instance = TransactionalEmailsApi(ApiClient(configuration))

    def create_website_theme_email(self, to_email, items, new_items_count, server_url="http://localhost:5001"):
        """Create exact terminal-style email matching the screenshot"""

        # Create terminal blocks for each store
        terminal_blocks = []

        for item in items:
            is_new = item.get('is_new', False)
            store_name_clean = item['store'].lower().replace(
                ' ', '').replace('&', '').replace('-', '').replace("'", '')

            if is_new:
                border_style = "border-left: 4px solid #ff4444;"
                status_badge = '<span style="background-color: #ff4444; color: #ffffff; padding: 3px 8px; font-size: 11px; font-weight: bold; text-transform: uppercase;">NEW!</span>'
            else:
                border_style = "border-left: 4px solid #4caf50;"
                status_badge = '<span style="background-color: #4caf50; color: #ffffff; padding: 3px 8px; font-size: 11px; font-weight: bold; text-transform: uppercase;">AVAILABLE</span>'

            terminal_blocks.append(f'''
            <div style="{border_style} background-color: #1a1a1a; margin: 0;">
                <div style="background-color: #1a1a1a; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #4caf50; font-weight: 600;">store@{store_name_clean}:~$</span>
                    <span style="color: #00bcd4; font-weight: 500; margin-left: 10px;">check_availability</span>
                    {status_badge}
                </div>
                <div style="background-color: #000000; padding: 20px 25px;">
                    <div style="color: #ffffff; font-weight: 600; font-size: 16px; margin-bottom: 8px;">🏪 {item['store']} • {item['item']}</div>
                    <div style="color: #888888; font-size: 14px; margin-bottom: 8px;">📍 {item['address']}</div>
                    <div style="color: #ffd700; font-weight: 600; font-size: 15px; margin-bottom: 15px;">💰 €{item['price']} • {item['available']} bags available</div>
                    <div style="color: #666666; font-size: 16px; padding-left: 25px;">...</div>
                </div>
            </div>
            ''')

        terminal_html = "".join(terminal_blocks)

        # Create properly encoded unsubscribe URL
        encoded_email = urllib.parse.quote_plus(to_email)
        unsubscribe_url = f"{server_url}/unsubscribe?email={encoded_email}"

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>TooGoodToGo Terminal Alert</title>
            <link href="https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@400;500;600&display=swap" rel="stylesheet">
        </head>
        <body style="font-family: 'Source Code Pro', 'Courier New', monospace; background-color: #000000; color: #ffffff; padding: 0; margin: 0; line-height: 1.4;">
            <div style="background-color: #000000; border: 2px solid #4caf50; margin: 20px auto; max-width: 800px; width: 95%;">
                
                <!-- System Header -->
                <div style="background-color: #000000; padding: 20px 25px; border-bottom: 1px solid #4caf50;">
                    <div style="color: #00bcd4; font-size: 18px; font-weight: 600;">
                        <span style="color: #ff4444; margin-right: 8px;">🚨</span>SYSTEM ALERT: {new_items_count} New Item(s) Available
                    </div>
                </div>

                <!-- Terminal Blocks -->
                {terminal_html}

                <!-- Action Buttons -->
                <div style="background-color: #000000; padding: 25px; text-align: center; border-top: 1px solid #333333;">
                    <a href="https://toogoodtogo.com/" style="background-color: #4caf50; color: #000000; text-decoration: none; padding: 12px 25px; font-family: 'Source Code Pro', monospace; font-weight: 600; font-size: 14px; text-transform: uppercase; display: inline-block; margin: 10px;">
                        🥯 Open TooGoodToGo App
                    </a>
                </div>

                <!-- Footer -->
                <div style="background-color: #000000; padding: 20px 25px; text-align: center; border-top: 1px solid #333333; font-size: 12px; color: #888888;">
                    <p>Happy food saving! 🌱</p>
                    <p>Together we're fighting food waste, one surprise bag at a time.</p>
                    <br>
                    <p>
                        <a href="{server_url}" style="color: #00bcd4; text-decoration: none;">Visit TooGoodToGo Terminal</a> | 
                        <a href="{unsubscribe_url}" style="color: #00bcd4; text-decoration: none;">Unsubscribe</a>
                    </p>
                </div>
            </div>
        </body>
        </html>
        """

    def send_notification(self, to_email, items, new_items_count, server_url="http://localhost:5001"):
        """Send clean terminal-style notification email"""
        email_html = self.create_website_theme_email(
            to_email, items, new_items_count, server_url)

        email = SendSmtpEmail(
            to=[{"email": to_email}],
            sender={"name": "TooGoodToGo Terminal",
                    "email": "samwhoreai@gmail.com"},
            subject=f"🚨 SYSTEM ALERT: {new_items_count} New Item(s) Available",
            html_content=email_html
        )

        try:
            self.api_instance.send_transac_email(email)
            print(
                f"✅ Terminal notification sent to {to_email} for {new_items_count} new stores")
            return True
        except ApiException as e:
            print(f"❌ Error sending email: {e}")
            return False
