import openai
import os
from dotenv import load_dotenv
import base64
import requests
 
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def image_to_desc(base64_image, openai_key, pl_theme="None",):
  openai.api_key = openai_key
  # base64_image = encode_image(image)
  #base64_image = base64.b64encode(image_file.read()).decode('utf-8')


  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}"
  }

  payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": f"""
            can you create a list of 20 songs that would match the setting portrayed in this image and/or to set the vibe 
            portrayed by this image, this is also the desired theme of the playlist {pl_theme}, use it to select recommendations.
            Also make sure to favour songs that are higher rated and more popular. 
            I just want you to list the results in this format ("song name": artist&), separated by commas and nothing 
            else in your response. Additionally give me a little desription of the image as a prompt to pass on to 
            DALL-E to make a cartoony version of the prompt as a playlist cover (put this part at the beginning of your 
            response and separate from the list using $&$). 

            Just a reminder: the form of your response should be 'Description$&$List_of_songs', where List_of_songs is in this format ("song name": artist&)

          """
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 500
  }

  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  # print(response.json())
  res1 = response.json()['choices'][0]['message']['content']
  return res1


# load_dotenv()
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# temp = base64.b64encode(open('images/sunset1.png', "rb").read()).decode('utf-8')
# print(temp)
# image_to_desc(temp, os.getenv('OPENAI_API_KEY'))