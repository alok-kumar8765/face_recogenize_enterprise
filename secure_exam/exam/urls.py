# exam/urls.py
from django.urls import path

from exam.views.face_only import face_only_verify
from exam.views.liveness_only import blink_only_verify
from exam.views.face_with_liveness import face_with_liveness
from exam.views.violation import log_violation

urlpatterns = [
    # ---- Verification Modes ----
    path("", face_with_liveness, name="exam_home"),
    path("face/", face_only_verify, name="face_only"),
    path("liveness/", blink_only_verify, name="liveness_only"),
    path("secure/", face_with_liveness, name="face_with_liveness"),

    # ---- Anti-Cheat ----
    path("violation/", log_violation, name="log_violation"),
]
