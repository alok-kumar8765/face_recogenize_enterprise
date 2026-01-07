from django.urls import path
from exam_proctor.views import (
    face_only,
    liveness_only,
    face_with_liveness,
    
)
from exam_proctor.views.violation import log_violations, log_violation
urlpatterns = [
    path("face/", face_only),
    path("liveness/", liveness_only),
    path("secure/", face_with_liveness),
    path("violation/", log_violation),
    path("violations/", log_violations),
]
