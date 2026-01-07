import mediapipe as mp
import numpy as np

mp_face = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# Eye landmark indexes
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

def detect_blink(rgb_frame, state):
    result = mp_face.process(rgb_frame)
    if not result.multi_face_landmarks:
        return False, state

    h, w, _ = rgb_frame.shape
    mesh = result.multi_face_landmarks[0].landmark

    left = np.array([(mesh[i].x * w, mesh[i].y * h) for i in LEFT_EYE])
    right = np.array([(mesh[i].x * w, mesh[i].y * h) for i in RIGHT_EYE])

    ear = (eye_aspect_ratio(left) + eye_aspect_ratio(right)) / 2

    if ear < 0.23:
        state['counter'] += 1
    else:
        if state['counter'] >= 2:
            state['blinks'] += 1
        state['counter'] = 0

    return state['blinks'] >= 1, state
