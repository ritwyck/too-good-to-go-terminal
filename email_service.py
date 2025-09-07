from sib_api_v3_sdk import ApiClient, Configuration, TransactionalEmailsApi, SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException


class EmailService:
    def __init__(self, api_key):
        configuration = Configuration()
        configuration.api_key['api-key'] = api_key
        self.api_instance = TransactionalEmailsApi(ApiClient(configuration))

    def create_website_theme_email(self, to_email, items, new_items_count, server_url="http://localhost:5001"):
        """Create professional email with website's dark mode colors"""

        # Create item HTML for each store
        html_lines = []
        for item in items:
            is_new = item.get('is_new', False)
            new_class = 'new' if is_new else ''
            new_badge = '<span class="new-badge">NEW!</span>' if is_new else ''

            html_lines.append(f"""
            <div class="item {new_class}">
                <div class="store-header">
                    <h3>🏪 {item['store']}</h3>
                    {new_badge}
                </div>
                <div class="item-details">
                    <p><strong>{item['item']}</strong></p>
                    <p>📍 {item['address']}</p>
                    <p>💰 €{item['price']} • <span class="availability">{item['available']} bags available</span></p>
                </div>
            </div>
            """)

        items_html = "".join(html_lines)

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
            <title>TooGoodToGo Alert</title>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box !important;
                }}

                body {{
                    font-family: 'JetBrains Mono', monospace;
                    background-color: #000000;
                    color: #f5f5f5;
                    line-height: 1.6;
                    margin: 0 !important;
                    padding: 10px !important;
                    width: 100% !important;
                    -webkit-text-size-adjust: 100% !important;
                    -ms-text-size-adjust: 100% !important;
                }}

                table {{
                    border-collapse: collapse !important;
                    mso-table-lspace: 0pt !important;
                    mso-table-rspace: 0pt !important;
                }}

                .email-container {{
                    width: 100% !important;
                    max-width: 600px !important;
                    margin: 0 auto !important;
                    background-color: #111111;
                    border: 2px solid #2e8b57;
                    border-radius: 12px;
                    overflow: hidden;
                    box-sizing: border-box !important;
                }}

                .header {{
                    background-color: #1a1a1a;
                    padding: 20px !important;
                    text-align: center;
                    border-bottom: 2px solid #2e8b57;
                }}

                .header h1 {{
                    color: #2e8b57;
                    font-size: 20px !important;
                    font-weight: 700;
                    margin-bottom: 10px;
                    word-wrap: break-word !important;
                }}

                .header p {{
                    color: #888888;
                    font-size: 12px !important;
                    word-wrap: break-word !important;
                }}

                .content {{
                    padding: 20px !important;
                }}

                .alert-section {{
                    background-color: #1a1a1a;
                    border: 1px solid #2e8b57;
                    border-radius: 8px;
                    padding: 20px !important;
                    text-align: center;
                    margin-bottom: 20px !important;
                    word-wrap: break-word !important;
                }}

                .alert-section h2 {{
                    color: #6bcf7f;
                    font-size: 16px !important;
                    font-weight: 700;
                    margin-bottom: 10px;
                    word-wrap: break-word !important;
                }}

                .alert-section p {{
                    color: #f5f5f5;
                    font-size: 14px !important;
                    word-wrap: break-word !important;
                }}

                .items-section {{
                    margin-bottom: 20px !important;
                }}

                .section-title {{
                    color: #20b2aa;
                    font-size: 16px !important;
                    font-weight: 700;
                    margin-bottom: 15px !important;
                    padding-bottom: 8px;
                    border-bottom: 1px solid #333333;
                    word-wrap: break-word !important;
                }}

                .item {{
                    background-color: #1a1a1a;
                    border: 1px solid #333333;
                    border-left: 4px solid #2e8b57;
                    border-radius: 8px;
                    padding: 15px !important;
                    margin-bottom: 15px !important;
                    transition: all 0.3s ease;
                    word-wrap: break-word !important;
                    overflow-wrap: break-word !important;
                    width: 100% !important;
                }}

                .item:hover {{
                    border-left-color: #20b2aa;
                    background-color: #1f1f1f;
                }}

                .item.new {{
                    border-left-color: #ff6b6b;
                    background-color: #1f1111;
                }}

                .item.new:hover {{
                    background-color: #241414;
                    border-left-color: #ff5252;
                }}

                .store-header {{
                    display: flex !important;
                    align-items: center;
                    justify-content: space-between;
                    margin-bottom: 12px !important;
                    flex-wrap: wrap !important;
                    width: 100% !important;
                }}

                .store-header h3 {{
                    color: #f5f5f5;
                    font-size: 16px !important;
                    font-weight: 700;
                    margin: 0;
                    word-wrap: break-word !important;
                    flex: 1;
                }}

                .item.new .store-header h3 {{
                    color: #ff8a80;
                }}

                .new-badge {{
                    background-color: #ff6b6b;
                    color: #000000;
                    padding: 4px 8px !important;
                    border-radius: 8px;
                    font-size: 10px !important;
                    font-weight: 700;
                    text-transform: uppercase;
                    margin-left: 8px !important;
                    white-space: nowrap;
                    flex-shrink: 0;
                }}

                .item-details p {{
                    margin: 6px 0 !important;
                    color: #888888;
                    font-size: 12px !important;
                    word-wrap: break-word !important;
                    overflow-wrap: break-word !important;
                }}

                .item-details p strong {{
                    color: #f5f5f5;
                    font-weight: 700;
                }}

                .availability {{
                    color: #ffd93d;
                    font-weight: 700;
                }}

                .button-section {{
                    text-align: center;
                    margin: 30px 0 !important;
                }}

                .button {{
                    display: inline-block !important;
                    background: linear-gradient(90deg, #2e8b57 0%, #20b2aa 100%);
                    color: white !important;
                    text-decoration: none !important;
                    padding: 12px 20px !important;
                    font-family: 'JetBrains Mono', monospace;
                    font-weight: 700;
                    font-size: 12px !important;
                    border-radius: 8px;
                    margin: 8px !important;
                    text-transform: uppercase;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(46, 139, 87, 0.3);
                    min-width: 120px;
                    box-sizing: border-box !important;
                }}

                .button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(46, 139, 87, 0.5);
                }}

                .button-secondary {{
                    background: linear-gradient(90deg, #ff6b6b 0%, #ff5252 100%) !important;
                    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
                    font-size: 11px !important;
                    padding: 10px 18px !important;
                }}

                .button-secondary:hover {{
                    box-shadow: 0 6px 20px rgba(255, 107, 107, 0.5);
                }}

                .footer {{
                    background-color: #0a0a0a;
                    padding: 20px !important;
                    text-align: center;
                    border-top: 1px solid #333333;
                }}

                .footer p {{
                    color: #888888;
                    font-size: 11px !important;
                    line-height: 1.6;
                    margin: 6px 0 !important;
                    word-wrap: break-word !important;
                }}

                .footer a {{
                    color: #20b2aa;
                    text-decoration: none;
                    word-wrap: break-word !important;
                }}

                .footer a:hover {{
                    text-decoration: underline;
                }}

                .divider {{
                    height: 1px;
                    background-color: #333333;
                    margin: 20px 0 !important;
                }}

                /* Mobile-first responsive design */
                @media only screen and (max-width: 480px) {{
                    body {{
                        padding: 5px !important;
                    }}

                    .email-container {{
                        border-radius: 8px !important;
                        border-width: 1px !important;
                    }}

                    .header, .content, .footer {{
                        padding: 15px !important;
                    }}

                    .header h1 {{
                        font-size: 18px !important;
                    }}

                    .store-header {{
                        flex-direction: column !important;
                        align-items: flex-start !important;
                        gap: 5px !important;
                    }}

                    .new-badge {{
                        margin-left: 0 !important;
                        margin-top: 5px !important;
                        align-self: flex-start !important;
                    }}

                    .item {{
                        padding: 12px !important;
                    }}

                    .button {{
                        display: block !important;
                        width: 90% !important;
                        max-width: 280px !important;
                        margin: 10px auto !important;
                        padding: 14px 20px !important;
                        font-size: 12px !important;
                    }}

                    .alert-section {{
                        padding: 15px !important;
                    }}

                    .alert-section h2 {{
                        font-size: 15px !important;
                    }}
                }}

                /* Tablet responsive design */
                @media only screen and (min-width: 481px) and (max-width: 768px) {{
                    .email-container {{
                        max-width: 90% !important;
                    }}

                    .header, .content, .footer {{
                        padding: 18px !important;
                    }}

                    .button {{
                        font-size: 13px !important;
                        padding: 13px 22px !important;
                    }}
                }}

                /* Desktop responsive design */
                @media only screen and (min-width: 769px) {{
                    .content {{
                        padding: 30px !important;
                    }}

                    .header {{
                        padding: 30px !important;
                    }}

                    .header h1 {{
                        font-size: 24px !important;
                    }}

                    .button {{
                        font-size: 14px !important;
                        padding: 15px 30px !important;
                    }}
                }}

                /* Fix for Outlook */
                .ExternalClass {{
                    width: 100% !important;
                }}

                .ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div {{
                    line-height: 100% !important;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <!-- Header -->
                <div class="header">
                    <h1>TooGoodToGo Terminal</h1>
                    <p>Your surprise bag notification service</p>
                </div>

                <!-- Content -->
                <div class="content">
                    <!-- Alert Section -->
                    <div class="alert-section">
                        <h2>🚨 New Surprise Bags Available!</h2>
                        <p>{new_items_count} new item(s) have been detected in your favorites</p>
                    </div>

                    <!-- Items Section -->
                    <div class="items-section">
                        <h2 class="section-title">Available Items</h2>
                        {items_html}
                    </div>

                    <!-- Action Button -->
                    <div class="button-section">
                        <a href="https://toogoodtogo.com/" class="button">
                            🥯 Open TooGoodToGo App
                        </a>
                    </div>

                    <div class="divider"></div>

                    <!-- Additional Info -->
                    <div class="alert-section">
                        <h2>How it works</h2>
                        <p style="text-align: left; color: #888888; font-size: 12px;">
                            • Our service monitors your TooGoodToGo favorites every minute<br>
                            • You only receive emails when new bags become available<br>
                            • Each email shows all currently available items from your favorites<br>
                            • Your data is encrypted and stored securely
                        </p>
                    </div>
                </div>

                <!-- Footer -->
                <div class="footer">
                    <p><strong>Happy food saving! 🌱</strong></p>
                    <p>Together we're fighting food waste, one surprise bag at a time.</p>
                    
                    <div class="button-section">
                        <a href="{server_url}/unsubscribe?email={to_email}" class="button button-secondary">
                            Unsubscribe from alerts
                        </a>
                    </div>
                    
                    <p>You're receiving this email because you subscribed to TooGoodToGo Terminal.</p>
                    <p><a href="{server_url}/unsubscribe?email={to_email}">Click here to unsubscribe</a></p>
                </div>
            </div>
        </body>
        </html>
        """

    def send_notification(self, to_email, items, new_items_count, server_url="http://localhost:5001"):
        """Send website-themed notification email"""
        email_html = self.create_website_theme_email(
            to_email, items, new_items_count, server_url)

        email = SendSmtpEmail(
            to=[{"email": to_email}],
            sender={"name": "TooGoodToGo Terminal",
                    "email": "samwhoreai@gmail.com"},
            subject=f"🚨 {new_items_count} New Surprise Bag(s) Available",
            html_content=email_html
        )

        try:
            self.api_instance.send_transac_email(email)
            print(
                f"✅ Notification sent to {to_email} for {new_items_count} new items")
            return True
        except ApiException as e:
            print(f"❌ Error sending email: {e}")
            return False
