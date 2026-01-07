import face_recognition
import numpy as np
import pickle

def encode_face(image_path):
    """
    Returns pickled face encoding if exactly ONE face is found.
    Raises ValueError otherwise.
    """
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)

    if len(encodings) != 1:
        raise ValueError("Exactly one face must be visible")

    encoding = encodings[0]
    return pickle.dumps(encoding)
