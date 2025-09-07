import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from dotenv import load_dotenv
import re
import time
import threading
from tgtg import TgtgClient
from models import db, User
from data_service import DatabaseService

# Load environment variables
load_dotenv()


def complete_auth_task(app, tgtg_email, data_service):
    with app.app_context():  # ✅ Explicit app reference
        try:
            client = TgtgClient(email=tgtg_email)
            print(f"🔐 Authentication started for {tgtg_email}")
            credentials = client.get_credentials()
            test_items = client.get_items()  # Test the connection
            # Create user with encrypted credentials
            user = data_service.create_user(tgtg_email, credentials)
            print(f"✅ User {tgtg_email} registered successfully!")
        except Exception as e:
            print(f"❌ Authentication failed for {tgtg_email}: {e}")


def create_app():
    app = Flask(__name__)

    # Load environment variables first
    load_dotenv()

    # Essential Flask configuration
    app.config['SECRET_KEY'] = os.getenv(
        'SECRET_KEY', 'dev-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'sqlite:///instance/tgtg_monitor.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access monitoring.'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Initialize database service
    data_service = DatabaseService()

    def is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            if not email or not password:
                return jsonify({"success": False, "message": "Email and password required"})
            user = data_service.get_user_by_email(email)
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                return jsonify({"success": False, "message": "Invalid credentials"})
        return render_template('login.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html', user=current_user)

    @app.route('/start_auth', methods=['POST'])
    def start_auth():
        tgtg_email = request.form.get('tgtg_email', '').strip()
        if not tgtg_email or not is_valid_email(tgtg_email):
            return jsonify({"success": False, "message": "Please enter a valid email address."})
        # Check if user already exists
        existing_user = data_service.get_user_by_email(tgtg_email)
        if existing_user:
            return jsonify({"success": False, "message": "This email is already registered!"})
        try:
            # Pass app explicitly to the thread
            from flask import current_app
            threading.Thread(
                target=complete_auth_task,
                args=(current_app._get_current_object(),
                      tgtg_email, data_service),
                daemon=True
            ).start()
            return jsonify({
                "success": True,
                "message": f"Please check your TooGoodToGo email ({tgtg_email}) on PC and click the verification link!"
            })
        except Exception as e:
            return jsonify({"success": False, "message": f"Error: {str(e)}"})

    @app.route('/deregister', methods=['POST'])
    @login_required
    def deregister():
        success = data_service.remove_user(current_user.email)
        logout_user()
        if success:
            return jsonify({"success": True, "message": "Successfully removed from notifications."})
        else:
            return jsonify({"success": False, "message": "Error removing account."})

    @app.route('/unsubscribe')
    def unsubscribe_page():
        email = request.args.get('email', '')
        if email:
            user = data_service.get_user_by_email(email)
            if user:
                data_service.disable_monitoring(user)
                return render_template('unsubscribe_success.html', email=email)
        return render_template('unsubscribe.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    # Create tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5001, debug=True)
