from PIL import Image
import io
import numpy as np
import requests


def load_image_from_url(url):
	response = requests.get(url, verify=False)
	img = Image.open(io.BytesIO(response.content))
	img = img.convert("RGB")
	img = np.array(img)
	return img

def load_image_from_formdata(data):
	img = Image.open(data)
	img = img.convert("RGB")
	img = np.array(img)
	return img

