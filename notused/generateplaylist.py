import spotipy
from dotenv import load_dotenv
import os
import requests
import json

endpoint_url = "https://api.spotify.com/v1/recommendations?"

# OUR FILTERS
limit=10
market="US"
seed_genres="indie"
target_danceability=0.9

token = ""


query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}&target_danceability={target_danceability}'

response =requests.get(query, 
               headers={"Content-Type":"application/json", 
                        f"Authorization":"Bearer "})


json_response = response.json()

for i in json_response['tracks']:
            print(f"\"{i['name']}\" by {i['artists'][0]['name']}")



user_id = "zyumn1"
endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
request_body = json.dumps({
          "name": "tester playlist",
          "description": "My first programmatic playlist, yooo!",
          "public": False # let's keep it between us - for now
        })
response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json", 
                        "Authorization":"Bearer "})