from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
import base64


def generate_image():
  client = OpenAI()

  response = client.images.generate(
    model="dall-e-3",
    prompt="A cartoon picture of an LS1 swapped Scion FRS",
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

image = generate_image()
compress_image(image, 'images/img3.jpg', quality=85)

compressed_image_b64 = compress_image_to_b64(image, quality=85)
print(compressed_image_b64)

