from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
import base64


def generate_image():
  client = OpenAI()

  response = client.images.generate(
    model="dall-e-3",
    prompt="I made an app that lets you take a picture of your environment/setting/landscape and upload it, the program will then create a playlist that matches the setting/theme of the photo and directly add the playlist to your spotify account. make me a simple circular logo that would be good. you can take inspiration from the spotify icon",
    size="1024x1024",
    quality="standard",
    n=1,
  )
  img_url = response.data[0].url
  response = requests.get(img_url)
  image = Image.open(BytesIO(response.content))

  return image

def compress_image(image, output_path, quality=85):
    image.save(output_path, format="PNG", quality=quality)

def compress_image_to_b64(image, quality=85):
    buffer = BytesIO()
    image.save(buffer, format="PNG", quality=quality)
    buffer.seek(0)
    image_b64 = base64.b64encode(buffer.read()).decode('utf-8')
    return image_b64

image = generate_image()
compress_image(image, 'images/icon9.png', quality=85)

compressed_image_b64 = compress_image_to_b64(image, quality=85)
print(compressed_image_b64)

