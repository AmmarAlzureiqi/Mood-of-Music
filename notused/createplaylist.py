import os
from dotenv import load_dotenv
from spotifyclient import SpotifyClient
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

AUTH_URL = os.getenv('AUTH_URL')
TOKEN_URL = os.getenv('TOKEN_URL')
API_BASE_URL = os.getenv('API_BASE_URL')


def main():

    # get playlist name from user and create playlist
    playlist_name = input("\nWhat's the playlist name? ")
    
    scope1 = 'playlist-modify-public'

    username = 'zyumn1'
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope1,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            username=username
        )
    )

    def create_playlist(sp, username, playlist_name, playlist_description):
        playlists = sp.user_playlist_create(username, playlist_name, description = playlist_description)

    create_playlist(sp, username, playlist_name, 'Test playlist created using python!')
    print(f"\nPlaylist was created successfully.")



if __name__ == "__main__":
    main()