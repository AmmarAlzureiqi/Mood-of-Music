import requests
import urllib.parse

from flask import Flask, redirect, request, jsonify, session, render_template, url_for
from datetime import datetime, timedelta
from playlist import Playlist
import os
from dotenv import load_dotenv

from spotifyclient import SpotifyClient
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('APP_SECRET_KEY')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

AUTH_URL = os.getenv('AUTH_URL')
TOKEN_URL = os.getenv('TOKEN_URL')
API_BASE_URL = os.getenv('API_BASE_URL')

@app.route('/')
def index():
    return "Welcome to my Spotify App <a href='/login'> Login with Spotify</a>"


@app.route('/login')
def login():
    scope = 'user-read-private user-read-email playlist-read-private playlist-modify-public'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)


@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args["error"]})

    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        return redirect('/playlistsform')

@app.route("/playlistsform")
def my_form():
    return render_template('form.html')
    
@app.route('/playlistsform', methods=['GET', 'POST'])
# def get_playlists():
#     if 'access_token' not in session:
#         return redirect('/login')
    
#     if datetime.now().timestamp() > session['expires_at']:
#         return redirect('/refresh-token')

#     headers = {
#         'Authorization': f"Bearer {session['access_token']}"
#     }

#     response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
#     playlists = response.json()

#     return jsonify(playlists)

def get_playlist_info(): #getting playlist name and image (to create mood)
    if 'access_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')
    print(request.method)
    if request.method == 'POST':
        pl_name = request.form['playlist_name']
        session['pl_name'] = pl_name 
        # return render_template('form.html', playlist_name=pl_name)
        return redirect('/playlists')

    print(request.form.get('playlist_name'))
    return render_template('form.html')

@app.route('/playlists', methods=['GET', 'POST'])
def create_playlist():
    pl_name = session['pl_name']
    #scope1 = 'playlist-modify-public'

    sp = spotipy.Spotify(auth=session['access_token'])
    user = sp.current_user()


    # username = 'zyumn1'
    # sp1 = spotipy.Spotify(
    #     auth_manager=SpotifyOAuth(
    #         scope=scope1,
    #         client_id=CLIENT_ID,
    #         client_secret=CLIENT_SECRET,
    #         redirect_uri=REDIRECT_URI,
    #         username=user['id']
    #     )
    # )
    def create_playlist(sp, username, playlist_name, playlist_description):
        playlists = sp.user_playlist_create(username, playlist_name, description = playlist_description)

    create_playlist(sp, user['id'], pl_name, 'Test playlist created using python!')
    print(f"\nPlaylist was created successfully.")
    return "this is a list"


@app.route('/refresh_token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'authorization_code',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data = req_body)
        new_token_info = response.json()

        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

        return redirect('/playlistsform')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port = 5001)




