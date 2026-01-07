from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

import json, pickle, cv2
import numpy as np

from candidates.models import Candidate
from exam.services.image_decoder import decode_base64_image
from exam.services.face_matcher import match_face
from exam.liveness.blink import detect_blink
from exam.liveness.head_move import detect_head_movement


def convert_state(obj):
    """
    Recursively convert NumPy types to native Python types for JSON serialization
    """
    if isinstance(obj, dict):
        return {k: convert_state(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_state(i) for i in obj]
    elif isinstance(obj, (np.integer, int)):
        return int(obj)
    elif isinstance(obj, (np.floating, float)):
        return float(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif obj is None:
        return None
    else:
        return obj


@csrf_exempt
def face_with_liveness(request):
    # ----------------------------
    # GET: Render UI
    # ----------------------------
    if request.method == 'GET':
        return render(request, 'exam/face_with_liveness.html')

    # ----------------------------
    # POST: Verify Liveness + Face
    # ----------------------------
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    try:
        data = json.loads(request.body)
        reg_id = data.get('reg_id')
        image_data = data.get('image')
        state = data.get('state')
    except Exception:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not reg_id or not image_data:
        return JsonResponse({'error': 'Missing reg_id or image'}, status=400)

    try:
        candidate = Candidate.objects.get(registration_id=reg_id)
    except Candidate.DoesNotExist:
        return JsonResponse({'error': 'Invalid registration ID'}, status=404)

    # Decode base64 image to OpenCV frame
    frame = decode_base64_image(image_data)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ----------------------------
    # Default State
    # ----------------------------
    if not state:
        state = {
            'blink': {'done': False, 'counter': 0, 'blinks': 0},
            'head': {'done': False, 'center_x': None, 'moved_left': False, 'moved_right': False}
        }

    # ----------------------------
    # STEP 1: BLINK DETECTION
    # ----------------------------
    if not state['blink']['done']:
        blink_ok, blink_state = detect_blink(rgb, state['blink'])
        state['blink'].update(blink_state)
        if blink_ok:
            state['blink']['done'] = True
            return JsonResponse({
                'step': 'blink',
                'message': '✅ Blink detected. Now turn your head left and right',
                'state': convert_state(state)
            })
        return JsonResponse({
            'step': 'blink',
            'message': '👀 Please blink your eyes',
            'state': convert_state(state)
        })

    # ----------------------------
    # STEP 2: HEAD MOVEMENT
    # ----------------------------
    if not state['head']['done']:
        head_ok, head_state = detect_head_movement(rgb, state['head'])
        state['head'].update(head_state)
        if head_ok:
            state['head']['done'] = True
            return JsonResponse({
                'step': 'head',
                'message': '✅ Head movement detected. Verifying face…',
                'state': convert_state(state)
            })
        return JsonResponse({
            'step': 'head',
            'message': '↔️ Turn your head LEFT then RIGHT',
            'state': convert_state(state)
        })

    # ----------------------------
    # STEP 3: FACE MATCH
    # ----------------------------
    try:
        success, dist = match_face(rgb, pickle.loads(candidate.face_encoding))
        if dist is None:
            success = False
            dist = 0.0
    except Exception:
        success = False
        dist = 0.0

    return JsonResponse({
        'step': 'face',
        'message': '✅ Face + Liveness Verified' if success else '❌ Face Mismatch',
        'face_match': bool(success),
        'distance': float(dist),
        'state': convert_state(state)
    })