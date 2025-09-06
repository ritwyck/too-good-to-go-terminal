from sib_api_v3_sdk import ApiClient, Configuration, TransactionalEmailsApi, SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException


class EmailService:
    def __init__(self, api_key):
        configuration = Configuration()
        configuration.api_key['api-key'] = api_key
        self.api_instance = TransactionalEmailsApi(ApiClient(configuration))

    def create_dark_theme_email(self, to_email, items, new_items_count, server_url="http://localhost:5000"):
        """Create sleek dark theme email template without banner"""

        # Create item HTML for each store
        html_lines = []
        for item in items:
            is_new = item.get('is_new', False)
            new_class = 'new' if is_new else ''
            new_badge = '<span style="background: #ff4444; color: black; padding: 3px 8px; border-radius: 10px; font-size: 11px; font-weight: bold; margin-left: 10px; text-transform: uppercase;">NEW!</span>' if is_new else ''

            html_lines.append(f"""
            <div class="item {new_class}">
                <h3>🏪 {item['store']}{new_badge}</h3>
                <div class="details">
                    <strong>{item['item']}</strong><br>
                    📍 {item['address']}<br>
                    💰 €{item['price']} • {item['available']} bags available
                </div>
            </div>
            """)

        items_html = "".join(html_lines)

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>TooGoodToGo Terminal Alert</title>
            <style>
                body {{
                    margin: 0;
                    padding: 20px;
                    font-family: 'JetBrains Mono', 'Courier New', monospace;
                    background-color: #000000;
                    color: #f5f5f5;
                    line-height: 1.6;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #111111;
                    border: 2px solid #2e8b57;
                    border-radius: 12px;
                    padding: 30px;
                    box-shadow: 0 0 25px rgba(46, 139, 87, 0.3);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                    color: #2e8b57;
                    font-weight: bold;
                    font-size: 16px;
                    border-bottom: 1px solid #333333;
                    padding-bottom: 20px;
                }}
                .terminal-prompt {{
                    color: #2e8b57;
                    font-weight: bold;
                    margin-bottom: 15px;
                }}
                .alert {{
                    background-color: #0a0a0a;
                    border: 1px solid #2e8b57;
                    border-radius: 8px;
                    padding: 20px;
                    text-align: center;
                    margin-bottom: 25px;
                    font-size: 18px;
                    font-weight: bold;
                    color: #6bcf7f;
                }}
                .items {{
                    margin-bottom: 30px;
                }}
                .item {{
                    background-color: #1a1a1a;
                    border-left: 4px solid #2e8b57;
                    padding: 18px;
                    margin-bottom: 15px;
                    border-radius: 8px;
                    transition: all 0.3s ease;
                }}
                .item:hover {{
                    background-color: #1f1f1f;
                    border-left-color: #20b2aa;
                }}
                .item.new {{
                    border-left-color: #ff6b6b;
                    background-color: #1f1111;
                }}
                .item.new:hover {{
                    background-color: #241414;
                    border-left-color: #ff5252;
                }}
                .item h3 {{
                    margin: 0 0 12px 0;
                    color: #f5f5f5;
                    font-size: 16px;
                    font-weight: bold;
                    display: flex;
                    align-items: center;
                    flex-wrap: wrap;
                }}
                .item.new h3 {{
                    color: #ff8a80;
                }}
                .details {{
                    color: #cccccc;
                    font-size: 14px;
                    line-height: 1.5;
                }}
                .button-container {{
                    text-align: center;
                    padding: 20px 0;
                }}
                .button {{
                    display: inline-block;
                    padding: 14px 28px;
                    margin: 10px;
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: 700;
                    font-size: 14px;
                    text-transform: uppercase;
                    transition: all 0.3s ease;
                    font-family: 'JetBrains Mono', 'Courier New', monospace;
                }}
                .button:hover {{
                    transform: translateY(-2px);
                }}
                .button.primary {{
                    background: linear-gradient(135deg, #2e8b57 0%, #20b2aa 100%);
                    box-shadow: 0 4px 15px rgba(46, 139, 87, 0.4);
                }}
                .button.primary:hover {{
                    box-shadow: 0 6px 20px rgba(46, 139, 87, 0.6);
                }}
                .button.unsubscribe {{
                    background: linear-gradient(135deg, #ff6b6b 0%, #ff5252 100%);
                    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
                    margin-top: 10px;
                    padding: 12px 24px;
                    font-size: 12px;
                }}
                .button.unsubscribe:hover {{
                    box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6);
                }}
                .footer {{
                    font-size: 12px;
                    color: #888888;
                    text-align: center;
                    padding: 20px 0;
                    border-top: 1px solid #333333;
                    margin-top: 30px;
                    line-height: 1.6;
                }}
                .footer a {{
                    color: #20b2aa;
                    text-decoration: none;
                }}
                .footer a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
          
                
                <div class="terminal-prompt">
                    tgtg@monitor:~$ ./send_alert # {new_items_count} new surprise bags detected
                </div>
                
                <div class="alert">
                    🚨 SYSTEM ALERT: {new_items_count} New Item(s) Available
                </div>

                <div class="items">
                    {items_html}
                </div>

                <div class="button-container">
                    <a href="https://toogoodtogo.com/" class="button primary">
                        🥯 Open TooGoodToGo App
                    </a>
                    <br>
                    <a href="{server_url}/unsubscribe?email={to_email}" class="button unsubscribe">
                        🗑️ Unsubscribe
                    </a>
                </div>

                <div class="footer">
                    <div class="terminal-prompt">tgtg@monitor:~$ echo "Happy food saving! 🌱"</div>
                    <p>You're receiving this alert because you subscribed to TooGoodToGo monitoring.</p>
                    <p>Together we're fighting food waste, one surprise bag at a time.</p>
                    <p><a href="{server_url}/unsubscribe?email={to_email}">Click here to unsubscribe</a></p>
                </div>
            </div>
        </body>
        </html>
        """

    def send_notification(self, to_email, items, new_items_count, server_url="http://localhost:5000"):
        """Send dark theme notification email"""
        email_html = self.create_dark_theme_email(
            to_email, items, new_items_count, server_url)

        email = SendSmtpEmail(
            to=[{"email": to_email}],
            sender={"name": "TGTG Terminal Monitor",
                    "email": "samwhoreai@gmail.com"},
            subject=f"🚨 TGTG Terminal Alert: {new_items_count} New Surprise Bag(s)",
            html_content=email_html
        )

        try:
            self.api_instance.send_transac_email(email)
            print(
                f"✅ Dark theme notification sent to {to_email} for {new_items_count} new items")
            return True
        except ApiException as e:
            print(f"❌ Error sending email: {e}")
            return False
