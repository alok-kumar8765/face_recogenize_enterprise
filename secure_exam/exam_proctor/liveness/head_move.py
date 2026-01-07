import mediapipe as mp

mp_face = mp.solutions.face_mesh.FaceMesh()

NOSE = 1

def detect_head_movement(rgb_frame, state):
    result = mp_face.process(rgb_frame)
    if not result.multi_face_landmarks:
        return False, state

    face = result.multi_face_landmarks[0].landmark
    nose_x = face[NOSE].x

    if state['center_x'] is None:
        state['center_x'] = nose_x
        return False, state

    if nose_x < state['center_x'] - 0.04:
        state['moved_left'] = True
    elif nose_x > state['center_x'] + 0.04:
        state['moved_right'] = True

    return state['moved_left'] and state['moved_right'], state
