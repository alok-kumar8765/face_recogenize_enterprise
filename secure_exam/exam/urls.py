from django.urls import path
from .views import exam_login, verify_face
from exam.views.violation import log_violation
from exam.views.face_verify import face_only_verify
from exam.views.liveness_blink import blink_only_verify
from exam.views.combined_verify import face_with_liveness

urlpatterns = [
    path('', exam_login, name='exam_login'),      # GET page
    path('verify/', verify_face, name='verify_face'),  # POST API
    
    path('face/', face_only_verify, name='face_only_verify'),
    path('liveness/', blink_only_verify, name='liveness_only'),
    path('secure/', face_with_liveness, name='face_with_liveness'),
   
    path("violation/", log_violation),

]
