import numpy as np

NOISE_THRESHOLD = 3000

def detect_noise(audio_chunk):
    """
    audio_chunk: numpy array from mic
    """
    volume = np.linalg.norm(audio_chunk)
    return volume > NOISE_THRESHOLD
