from flask import Flask, redirect, request
from google.auth.transport import requests
from oauthlib.oauth2 import WebApplicationClient
import requests
import json

app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'
GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration'
GOOGLE_CLIENT_ID = '1090206121272-thig8rckgnrt36io53a125dr8ptd03vg.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
app.config['GOOGLE_CLIENT_ID'] = GOOGLE_CLIENT_ID
app.config['GOOGLE_CLIENT_SECRET'] = GOOGLE_CLIENT_SECRET
app.config['GOOGLE_DISCOVERY_URL'] = GOOGLE_DISCOVERY_URL

# oauth2 setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
    token_endpoint,
    authorization_response=request.url,
    redirect_url=request.base_url,
    code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/user')
def user():
    user_info = session.get('user_info', None)
    if user_info is None:
        return redirect('/login')
    return jsonify(user_info)

if __name__ == '__main__':
    app.run()