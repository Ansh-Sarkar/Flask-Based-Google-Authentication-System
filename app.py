from flask import Flask , url_for , redirect , session
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.secret_key='<secret_key>'

#oauth configuration for google login
oauth = OAuth(app)
google=oauth.register(
    name='google',
    client_id='',
    client_secret='',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope':'openid profile email'},
)

@app.route('/')
def hello_world():
    email=dict(session).get('email',None)
    return f'Hello, {email} !'


@app.route('/login')
def login():
    google=oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google=oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo',token=token)
    user_info = resp.json()
    # do something with the token and profile
    session['email']=user_info['email']
    return redirect('/')

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')