import json
import os
import requests
from flask import Blueprint, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from oauthlib.oauth2 import WebApplicationClient

# Disable HTTPS requirement for local development only
if os.environ.get('FLASK_ENV') == 'development' or not os.environ.get('REPLIT_DEV_DOMAIN'):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Determine the redirect URL based on environment
if os.environ.get("REPLIT_DEV_DOMAIN"):
    DEV_REDIRECT_URL = f'https://{os.environ.get("REPLIT_DEV_DOMAIN")}/google_login/callback'
else:
    # Local development
    DEV_REDIRECT_URL = 'http://localhost:5000/google_login/callback'

if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    print(f"""
    ═══════════════════════════════════════════════════════════
    Google OAuth Configuration:
    1. Go to https://console.cloud.google.com/apis/credentials
    2. Select your OAuth 2.0 Client ID
    3. Add {DEV_REDIRECT_URL} to Authorized redirect URIs
    4. Save the changes
    
    Current redirect URI: {DEV_REDIRECT_URL}
    ═══════════════════════════════════════════════════════════
    """)

client = WebApplicationClient(GOOGLE_CLIENT_ID) if GOOGLE_CLIENT_ID else None

google_auth = Blueprint("google_auth", __name__)


@google_auth.route("/google_login")
def login():
    if not GOOGLE_CLIENT_ID:
        flash('Google OAuth is not configured. Please contact the administrator.', 'error')
        return redirect(url_for('user_login'))
    
    try:
        google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Generate and store state parameter for CSRF protection
        import secrets
        state = secrets.token_urlsafe(32)
        from flask import session as flask_session
        flask_session['oauth_state'] = state

        # Use the correct redirect URI based on environment
        redirect_uri = request.base_url + "/callback"
        # Only use https if on Replit or production
        if os.environ.get("REPLIT_DEV_DOMAIN") or request.url.startswith("https://"):
            redirect_uri = redirect_uri.replace("http://", "https://")

        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=redirect_uri,
            scope=["openid", "email", "profile"],
            state=state,
        )
        return redirect(request_uri)
    except Exception as e:
        flash(f'Error connecting to Google: {str(e)}', 'error')
        return redirect(url_for('user_login'))


@google_auth.route("/google_login/callback")
def callback():
    # Import here to avoid circular import
    from app import db, User
    
    if not GOOGLE_CLIENT_ID:
        flash('Google OAuth is not configured. Please contact the administrator.', 'error')
        return redirect(url_for('user_login'))
    
    try:
        # Verify state parameter for CSRF protection
        from flask import session as flask_session
        state = request.args.get("state")
        stored_state = flask_session.pop('oauth_state', None)
        
        if not state or state != stored_state:
            flash('Invalid state parameter. Please try logging in again.', 'error')
            return redirect(url_for('user_login'))
        
        code = request.args.get("code")
        if not code:
            error = request.args.get("error")
            flash(f'Google authentication failed: {error}', 'error')
            return redirect(url_for('user_login'))
        
        google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
        token_endpoint = google_provider_cfg["token_endpoint"]

        # Use the correct redirect URI based on environment
        authorization_response = request.url
        redirect_url = request.base_url
        # Only use https if on Replit or production
        if os.environ.get("REPLIT_DEV_DOMAIN") or request.url.startswith("https://"):
            authorization_response = authorization_response.replace("http://", "https://")
            redirect_url = redirect_url.replace("http://", "https://")

        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=authorization_response,
            redirect_url=redirect_url,
            code=code,
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )

        if token_response.status_code != 200:
            flash(f'Failed to get access token: {token_response.text}', 'error')
            return redirect(url_for('user_login'))

        client.parse_request_body_response(json.dumps(token_response.json()))

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        if userinfo_response.status_code != 200:
            flash('Failed to get user information from Google.', 'error')
            return redirect(url_for('user_login'))

        userinfo = userinfo_response.json()
        if userinfo.get("email_verified"):
            users_email = userinfo["email"]
            users_name = userinfo.get("given_name", userinfo.get("name", "User"))
        else:
            flash("User email not available or not verified by Google.", "error")
            return redirect(url_for('user_login'))

        user = User.query.filter_by(email=users_email).first()
        if not user:
            user = User(username=users_name, email=users_email)
            db.session.add(user)
            db.session.commit()
            flash(f'Welcome {users_name}! Your account has been created.', 'success')
        else:
            flash(f'Welcome back, {user.username}!', 'success')

        login_user(user)

        return redirect(url_for('home'))
    
    except Exception as e:
        flash(f'Authentication error: {str(e)}', 'error')
        return redirect(url_for('user_login'))


@google_auth.route("/user/logout")
@login_required
def user_logout():
    from flask import session as flask_session
    logout_user()
    # Clear session data
    flask_session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))
