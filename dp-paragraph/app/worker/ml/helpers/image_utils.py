
import requests
import numpy as np
from PIL import Image
from io import BytesIO


def read_image_from_path_to_numpy(path):
    image = Image.open(path)
    image = image.convert('RGB')
    return np.asarray(image)


def read_image_from_dir(path) -> Image.Image:
    image = Image.open(path)
    return image


def read_bytes_image_from_url(url):
    response = requests.get(url)
    image_bytes = BytesIO(response.content)
    return image_bytes.read()


def read_image_from_url(url):
    im = Image.open(requests.get(url, stream=True).raw)
    return im


def io_bytes_to_numpy(io_bytes):
    image = Image.open(BytesIO(io_bytes))
    image = image.convert('RGB')
    return  np.asarray(image)


def numpy_to_io_bytes(numpy_image):
    pil_im = Image.fromarray(numpy_image)
    b = BytesIO()
    pil_im.save(b, 'jpeg')
    im_bytes = b.getvalue()
    return im_bytes