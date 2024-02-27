import openai
import os
from dotenv import load_dotenv
import base64
import requests
 
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "images/sunset1.png"

load_dotenv()

openai.api_key = os.getenv('API_KEY')


base64_image = encode_image(image_path)


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
          "text": "can you create a list of songs that would match the setting portrayed in this image and/or to set the vibe portrayed by this image. Also make sure to favour songs that are higher rated and more popular. I just wont you to list the results separated by commas"
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
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
res1 = response.json()['choices'][0]['message']['content']
print(res1)

