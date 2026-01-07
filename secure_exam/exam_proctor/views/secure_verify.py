from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

import json, pickle, cv2

from candidates.models import Candidate
from exam.services.image_decoder import decode_base64_image
from exam.services.face_matcher import match_face
from exam.liveness.blink import detect_blink
from exam.liveness.head_move import detect_head_movement


@csrf_exempt
def secure_verify(request):

    # ----------------------------
    # UI
    # ----------------------------
    if request.method == "GET":
        return render(request, "exam/secure_verify.html")

    # ----------------------------
    # API
    # ----------------------------
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    reg_id = data.get("reg_id")
    image = data.get("image")
    state = data.get("state")

    if not reg_id or not image:
        return JsonResponse({"error": "Missing reg_id or image"}, status=400)

    try:
        candidate = Candidate.objects.get(registration_id=reg_id)
    except Candidate.DoesNotExist:
        return JsonResponse({"error": "Invalid registration ID"}, status=404)

    frame = decode_base64_image(image)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ----------------------------
    # DEFAULT STATE (JSON SAFE)
    # ----------------------------
    if not state:
        state = {
            "blink": {"done": False, "counter": 0, "blinks": 0},
            "head": {
                "done": False,
                "center_x": None,
                "moved_left": False,
                "moved_right": False
            }
        }

    # ----------------------------
    # STEP 1 — BLINK
    # ----------------------------
    if not state["blink"]["done"]:
        blink_ok, blink_state = detect_blink(rgb, state["blink"])
        state["blink"].update(blink_state)

        if blink_ok:
            state["blink"]["done"] = True

        return JsonResponse({
            "step": "blink",
            "blink": state["blink"]["done"],
            "head": False,
            "face": False,
            "verified": False,
            "message": "Blink detected" if state["blink"]["done"] else "Please blink",
            "state": state
        })

    # ----------------------------
    # STEP 2 — HEAD MOVE
    # ----------------------------
    if not state["head"]["done"]:
        head_ok, head_state = detect_head_movement(rgb, state["head"])
        state["head"].update(head_state)

        if head_ok:
            state["head"]["done"] = True

        return JsonResponse({
            "step": "head",
            "blink": True,
            "head": state["head"]["done"],
            "face": False,
            "verified": False,
            "message": "Head movement detected" if state["head"]["done"] else "Turn head left & right",
            "state": state
        })

    # ----------------------------
    # STEP 3 — FACE MATCH
    # ----------------------------
    success, dist = match_face(
        rgb,
        pickle.loads(candidate.face_encoding)
    )

    return JsonResponse({
        "step": "face",
        "blink": True,
        "head": True,
        "face": bool(success),
        "verified": bool(success),
        "distance": round(float(dist), 4) if dist is not None else None,
        "message": "Verification successful" if success else "Face mismatch",
        "state": state
    })
