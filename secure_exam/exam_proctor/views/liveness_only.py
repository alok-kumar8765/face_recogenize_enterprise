from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, cv2

from exam.services.image_decoder import decode_base64_image
from exam.liveness.blink import detect_blink


@csrf_exempt
def blink_only_verify(request):
    if request.method == 'GET':
        return render(request, 'exam/liveness_only.html')

    data = json.loads(request.body)
    frame = decode_base64_image(data['image'])
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    detected, state = detect_blink(
        rgb, data.get('state', {'counter': 0, 'blinks': 0})
    )

    return JsonResponse({
        'blink_detected': detected,
        'state': state
    })
