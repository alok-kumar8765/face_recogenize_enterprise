import face_recognition

def detect_multiple_faces(rgb):
    faces = face_recognition.face_locations(rgb)
    return len(faces) > 1
