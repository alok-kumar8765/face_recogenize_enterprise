import base64
import cv2
import numpy as np

def decode_base64_image(data_url):
    header, encoded = data_url.split(',', 1)
    image_bytes = base64.b64decode(encoded)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
