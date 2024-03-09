import requests
import urllib.parse

from flask import Flask, redirect, request, jsonify, session, render_template, url_for
from datetime import datetime, timedelta
# from playlist import Playlist
import os
from dotenv import load_dotenv

# from spotifyclient import SpotifyClient
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from imagetodesc import image_to_desc
# from werkzeug.utils import secure_filename
import base64
from utils import create_playlist_fun




load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('APP_SECRET_KEY')

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

AUTH_URL = os.getenv('AUTH_URL')
TOKEN_URL = os.getenv('TOKEN_URL')
API_BASE_URL = os.getenv('API_BASE_URL')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return "Welcome to my Spotify App <a href='/login'> Login with Spotify</a>"


@app.route('/login')
def login():
    scope = 'user-read-private user-read-email playlist-read-private playlist-modify-public playlist-modify-private ugc-image-upload'

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
def get_playlist_info(): #getting playlist name and image (to create mood)
    if 'access_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    print(request.method)
    if request.method == 'POST':
        pl_name = request.form['playlist_name']
        playlist_image = request.files['img']

    else:
        pl_name = request.form.get('playlist_name')
        playlist_image = request.files.get('img')
    
    session['pl_name'] = pl_name 
    temp = base64.b64encode(playlist_image.read()).decode('utf-8') 
    result1 = image_to_desc(temp, OPENAI_API_KEY)
    session['playlist_image'] = result1

    return redirect('/playlists')


@app.route('/playlists', methods=['GET', 'POST'])
def create_playlist():
    pl_name = session['pl_name']

    sp = spotipy.Spotify(auth=session['access_token'])
    user = sp.current_user()


    response1 = session['playlist_image'].split('$&$')
    prompt = response1[0]
    songlist = response1[1].split('&,')
    create_playlist_fun(sp, user['id'], pl_name, 'Test playlist created using python!')
    list_of_songs = []

    for songitem in songlist:
        print(songitem)
        songitem = songitem.replace("\n","").split(': ')
        song = songitem[0]
        artist = songitem[1]
        songsearch = sp.search(q=song)
        list_of_songs.append(songsearch['tracks']['items'][0]['uri'])

    preplaylist =sp.user_playlists(user=user['id'])
    #print(preplaylist['items'][0]['id'])
    pplaylist = preplaylist['items'][0]['id']
    session['plst_name'] = pplaylist
    sp.user_playlist_add_tracks(user = user['id'], playlist_id=pplaylist, tracks=list_of_songs)

    with open("images/temp1.jpg", "rb") as image_file:  # opening file safely
        image_64_encode = base64.b64encode(image_file.read())
    
    if len(image_64_encode) > 256000: # check if image is too big
        print("Image is too big: ", len(image_64_encode))
    else:
        sp.playlist_upload_cover_image(pplaylist, image_64_encode)
        print("Image added.")



    
    #print(f"\nPlaylist was created successfully.")
    return redirect('/curatedplaylist')

@app.route('/curatedplaylist', methods=['GET', 'POST'])
def display_curatedplaylist():
    #print(session['playlist_image'])
    plst = f"https://open.spotify.com/embed/playlist/{session['plst_name']}?utm_source=generator&theme=0"
    return render_template('listpl.html', plst_url=plst)



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




