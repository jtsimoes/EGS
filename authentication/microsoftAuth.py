# config.py

CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'http://localhost:5000/callback'
AUTHORITY = 'https://login.microsoftonline.com/your_tenant_id'
SCOPE = ['https://graph.microsoft.com/.default']

# main.py
# pip install requests msal
import requests
from flask import Flask, redirect, request, session
from msal import ConfidentialClientApplication
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTHORITY, SCOPE

app = Flask(__name__)
app.secret_key = 'some_random_secret_key'

@app.route('/')
def index():
    session['state'] = 'some_random_state'
    auth_url = _build_auth_url(state=session['state'])
    return redirect(auth_url)

@app.route('/callback')
def callback():
    if request.args.get('state') != session.get('state'):
        return 'State mismatch', 400

    if 'error' in request.args:
        return request.args.get('error_description'), 400

    auth_code = request.args.get('code')
    result = _build_msal_app().acquire_token_by_authorization_code(
        auth_code,
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI
    )

    if 'error' in result:
        return result['error_description'], 400

    session['access_token'] = result['access_token']
    return 'Access token: {}'.format(session['access_token'])

def _build_msal_app():
    return ConfidentialClientApplication(
        CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY
    )

def _build_auth_url(state):
    return _build_msal_app().get_authorization_request_url(SCOPE, state=state, redirect_uri=REDIRECT_URI)

if __name__ == '__main__':
    app.run(debug=True)
