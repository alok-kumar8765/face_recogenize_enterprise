from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import base64
import json
import pickle
import numpy as np
import cv2
import face_recognition

from candidates.models import Candidate


@csrf_exempt
def face_only_verify(request):
    """
    GET  -> Render webcam page
    POST -> Verify face (legacy-compatible)
    """

    # ----------------------------
    # GET: Open webcam UI
    # ----------------------------
    if request.method == 'GET':
        return render(request, 'exam/face_only.html')

    # ----------------------------
    # POST: Verify face
    # ----------------------------
    if request.method != 'POST':
        return JsonResponse({'message': 'Invalid request'}, status=400)

    try:
        data = json.loads(request.body)
        reg_id = data.get('reg_id')
        image_data = data.get('image')
    except Exception:
        return JsonResponse({'message': 'Invalid data format'}, status=400)

    if not reg_id or not image_data:
        return JsonResponse({'message': 'Missing registration ID or image'}, status=400)

    try:
        candidate = Candidate.objects.get(registration_id=reg_id)
    except Candidate.DoesNotExist:
        return JsonResponse({'message': 'Invalid Registration ID'}, status=404)

    # ----------------------------
    # Decode base64 image (SAME AS LEGACY)
    # ----------------------------
    try:
        header, encoded = image_data.split(',', 1)
        image_bytes = base64.b64decode(encoded)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception:
        return JsonResponse({'message': 'Image decode failed'}, status=400)

    # ----------------------------
    # Convert to RGB (SAME AS LEGACY)
    # ----------------------------
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ----------------------------
    # Face encoding (SAME AS LEGACY)
    # ----------------------------
    encodings = face_recognition.face_encodings(rgb_frame)

    if len(encodings) != 1:
        return JsonResponse({
            'message': 'Face not clear or multiple faces detected'
        })

    live_encoding = encodings[0]
    stored_encoding = pickle.loads(candidate.face_encoding)

    # ----------------------------
    # Compare faces (SAME AS LEGACY)
    # ----------------------------
    distance = face_recognition.face_distance(
        [stored_encoding], live_encoding
    )[0]

    if distance <= 0.6:
        return JsonResponse({
            'message': '✅ Face Verified',
            'face_match': True,
            'distance': round(float(distance), 4)
        })
    else:
        return JsonResponse({
            'message': '❌ Face Mismatch',
            'face_match': False,
            'distance': round(float(distance), 4)
        })