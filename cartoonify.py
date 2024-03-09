import openai
import os
from dotenv import load_dotenv
import base64
import requests
 
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def cartoonifyimage(base64_image, openai_key):
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
            "text": 'Can you cartoonify this image?'
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
  res1 = response.json()['choices'][0]['message']['content']
  return res1


load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
temp = base64.b64encode(open('images/sunset1.png', "rb").read()).decode('utf-8')
print(temp)

#res = cartoonifyimage(temp, os.getenv('OPENAI_API_KEY'))
#print(res)

from openai import OpenAI
client = OpenAI()

response = client.images.generate(
  model="dall-e-3",
  prompt="A cartoon picture of a pyramid",
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
print(image_url)
response_image = requests.get(image_url)
print(response_image.content)
with open('images/img.jpg','wb') as f:
    f.write(response_image.content)