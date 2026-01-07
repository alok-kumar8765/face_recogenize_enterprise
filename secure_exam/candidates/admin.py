from django.contrib import admin
from .models import Candidate
from .services.face_encoder import encode_face

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('registration_id', 'full_name', 'created_at')
    search_fields = ('registration_id', 'full_name')

    def save_model(self, request, obj, form, change):
        if obj.photo and not obj.face_encoding:
            try:
                obj.face_encoding = encode_face(obj.photo.path)
            except Exception as e:
                self.message_user(request, f"Face encoding failed: {e}", level='ERROR')
                return
        super().save_model(request, obj, form, change)
