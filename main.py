from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import oi, request

app = Flask(__name__)

# Secret key for session management
app.secret_key = os.urandom(24)

# Configuration for Google OAuth
app.config['GOOGLE_CLIENT_ID'] = '1******m'
app.config['GOOGLE_CLIENT_SECRET'] = 'G******H'
app.config['GOOGLE_DISCOVERY_URL'] = 
oauth = OAuth(app)

# Create a Google OAuth client
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",

    # authorize_url='https://accounts.google.com/o/oauth2/auth',
    # authorize_params=None,
    # access_token_url='https://accounts.google.com/o/oauth2/token',
    # refresh_token_url=None,
    client_kwargs={'scope': 'openid profile 

google_config_url = "https://accounts.google.com/.well-known/openid-configuration"
response = requests.get(google_config_url)
config = response.json()
print('config is something ',config)  # Check if 'jwks_uri' is present


@app.route('/')
def home():
    return 'Welcome! <a href="/login">Login with Google</a>'

@app.route('/login')
def login():
    # Redirect to Google for authentication
    redirect_uri = 'http://localhost:5000/auth' 
    print('Redirect URI:', redirect_uri)  # Corrected print statement
    return google.authorize_redirect(redirect_uri)



@app.route('/auth')
def auth():
    # Get the user's information from Google
    token = google.authorize_access_token()
    print('Token:', token)  # Debugging the token

    # Extract nonce from the token
    nonce = token.get('nonce')
    print('Nonce:', nonce)  # Debugging nonce

    # Parse the ID token, passing the nonce
    user = google.parse_id_token(token, nonce=nonce)
    print('User:', user)  # Debugging user information

    # Store the user info in session
    session['user'] = user
    return redirect(url_for('profile'))



@app.route('/profile')
def profile():
    user = session.get('user')
    print('User Profile:', user)  # Debugging the user profile data
    if user:
        return f'Hello, {user["name"]}!'
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


