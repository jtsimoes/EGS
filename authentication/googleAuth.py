import os
import requests
import json
from flask import Flask, request, redirect, session, url_for, abort
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google
from pip._vendor import cachecontrol

app = Flask(__name__)
app.secret_key = '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'

GOOGLE_CLIENT_ID = '1090206121272-thig8rckgnrt36io53a125dr8ptd03vg.apps.googleusercontent.com'

# Configure the Google OAuth2 client
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid']
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Disable OAuthlib's HTTPS verification in development environment
flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri="http://localhost:5000/oauth2callback")

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return redirect("authorize")
        return function()
    return wrapper

@app.route("/")
def index():
    return redirect("login")
    # return "Hello World <a href='/login'><button>Login</button></a>"

@app.route("/login")
def login():
    # Generate the Google OAuth2 authorization URL
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/oauth2callback")
def oauth2callback():
    # Handle the Google OAuth2 response
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)
    
    
    id_info = id_token.verify_oauth2_token(
        id_token=credentials.id_token,
        request = token_request,
        clock_skew_in_seconds=1
    )
    
    session["name"] = id_info["name"]
    session["email"] = id_info["email"]
    session["google_id"] = id_info["sub"]
    session["token"] = credentials.token
    session["refresh_token"] = credentials.refresh_token
    session["token_uri"] = credentials.token_uri
    session["client_id"] = credentials.client_id
    session["client_secret"] = credentials.client_secret
    session["scopes"] = credentials.scopes
    
    
    return redirect("user_info")

@app.route("/logout")
def logout():
    credentials = Credentials.from_authorized_user_info(session, SCOPES)

    # Revoke token
    requests.post('https://oauth2.googleapis.com/revoke',
                    params={'token': credentials.token},
                    headers={'content-type': 'application/x-www-form-urlencoded'})

    # Clear session
    session.clear()
      
    return redirect("/")

@app.route("/user_info")
@login_is_required
def user_info():
    return f"user: {session['name']}<BR>email: {session['email']}<BR>google_id: {session['google_id']}<BR>token: {session['token']}"
    # logout <a href='/logout'><button>Logout</button></a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
