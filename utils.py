import spotipy
import requests
from openai import OpenAI
import openai
from PIL import Image
from io import BytesIO
import base64

def image_to_desc(base64_image, openai_key, pl_theme="None"):
    openai.api_key = openai_key

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": f"""
                can you create a list of 20 songs that would match the setting portrayed in this image and/or to set the vibe 
                portrayed by this image use it to select recommendations.
                Also make sure to favour songs that are higher rated and more popular. I need a minimum of 15 songs.
                I just want you to list the results in this format ("song name": artist&), separated by commas and nothing 
                else in your response. Additionally give me a little description of the image as a prompt to pass on to 
                DALL-E to make a cartoony version of the prompt as a playlist cover (put this part at the beginning of your 
                response and separate from the list using $&$). 
                Just a reminder: the form of your response should be 'Description$&$List_of_songs', where List_of_songs is in this format ("song name": artist&)
                """
            },
            {
                "role": "user",
                "content": f"data:image/jpeg;base64,{base64_image}"
            }
        ],
        "max_tokens": 500
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())  # For debugging
    try:
        res1 = response.json()['choices'][0]['message']['content']
        return res1
    except KeyError:
        print("KeyError: 'choices' not found in the response.")
        return None


def create_playlist_fun(sp, username, playlist_name, playlist_description):
    playlists = sp.user_playlist_create(username, playlist_name, description = playlist_description, public=True)

def generate_image(prmt):
  client = OpenAI()

  response = client.images.generate(
    model="dall-e-3",
    prompt=f"A cartoon picture of this description: {prmt}",
    size="1024x1024",
    quality="standard",
    n=1,
  )
  img_url = response.data[0].url
  response = requests.get(img_url)
  image = Image.open(BytesIO(response.content))

  return image

def compress_image(image, output_path, quality=85):
    image.save(output_path, format="JPEG", quality=quality)

def compress_image_to_b64(image, quality=85):
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)
    image_b64 = base64.b64encode(buffer.read()).decode('utf-8')
    return image_b64