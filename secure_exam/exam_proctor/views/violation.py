from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from exam_proctor.models import ProctorViolation


@csrf_exempt
def log_violation(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    violation = data.get("type")
    count = int(data.get("count", 1))

    action = "LOGGED"

    # 🔥 TERMINATION RULES
    if violation == "TAB_SWITCH" and count >= 3:
        action = "TERMINATE"

    if violation in ["CAMERA_OFF", "MULTIPLE_FACES"]:
        action = "TERMINATE"

    return JsonResponse({
        "violation": violation,
        "count": count,
        "action": action
    })

@csrf_exempt
def log_violations(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body)

    ProctorViolation.objects.create(
        type=data.get("type"),
        metadata=data
    )

    return JsonResponse({"status": "logged"})