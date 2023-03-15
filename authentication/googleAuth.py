import os
import requests
import json
from flask import Flask, request, redirect, session, url_for
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")

# Configure the Google OAuth2 client
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Disable OAuthlib's HTTPS verification in development environment
flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
flow.redirect_uri = "http://localhost:5000/oauth2callback"


@app.route("/")
def index():
    if "credentials" not in session:
        return redirect("authorize")

    credentials = Credentials.from_authorized_user_info(
        session["credentials"], scopes=SCOPES
    )

    # Call the Google Drive API to list the user's files
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {credentials.token}"
    }
    r = requests.get("https://www.googleapis.com/drive/v3/files", headers=headers)
    files = r.json().get("files", [])

    return f"You have {len(files)} files in your Google Drive"


@app.route("/authorize")
def authorize():
    # Generate the Google OAuth2 authorization URL
    authorization_url = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )[0]

    return redirect(authorization_url)


@app.route("/oauth2callback")
def oauth2callback():
    # Handle the Google OAuth2 response
    flow.fetch_token(authorization_response=request.url)

    # Store the user's credentials in the session
    session["credentials"] = credentials_to_dict(flow.credentials)
    print(session["credentials"])
    return redirect(url_for("index"))


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

@app.route("/logout")
def logout():
    # Remove the user's credentials from the session
    if 'credentials' in session:
        credentials = Credentials.from_authorized_user_info(session['credentials'])
    revoke_google_tokens(credentials)

    return redirect(url_for("index"))

def revoke_google_tokens(credentials):
    # Build and authorize a client object for the credentials.
    client = credentials.authorize(httplib2.Http())
    
    # Revoke the access token associated with the credentials.
    if credentials.token:
        revoke_uri = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % credentials.token
        response = client.request(revoke_uri, method='GET')
        
        if response.status == 200:
            del credentials.token
            return True
    
    return False

if __name__ == "__main__":
    app.run(debug=True)
