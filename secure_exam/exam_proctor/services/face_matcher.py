import face_recognition

THRESHOLD = 0.6

def match_face(rgb_frame, stored_encoding):
    encodings = face_recognition.face_encodings(rgb_frame)

    if len(encodings) != 1:
        return False, None

    live_encoding = encodings[0]
    distance = face_recognition.face_distance(
        [stored_encoding], live_encoding
    )[0]

    return distance <= THRESHOLD, distance
