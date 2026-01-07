from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json, pickle, cv2

from candidates.models import Candidate
from exam.services.image_decoder import decode_base64_image
from exam.services.face_matcher import match_face


def exam_login(request):
    return render(request, 'exam/verify.html')


@csrf_exempt
def verify_face(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    data = json.loads(request.body)
    reg_id = data.get('reg_id')
    image = data.get('image')

    if not reg_id or not image:
        return JsonResponse({'error': 'Missing data'}, status=400)

    try:
        candidate = Candidate.objects.get(registration_id=reg_id)
    except Candidate.DoesNotExist:
        return JsonResponse({'error': 'Invalid Registration ID'}, status=404)

    frame = decode_base64_image(image)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    success, dist = match_face(rgb, pickle.loads(candidate.face_encoding))

    if dist is None:
        return JsonResponse({'error': 'Face not clear or multiple faces detected'})

    return JsonResponse({
        'verified': success,
        'distance': round(float(dist), 4)
    })
