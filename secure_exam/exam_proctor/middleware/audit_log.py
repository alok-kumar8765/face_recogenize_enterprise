import time
from django.utils.deprecation import MiddlewareMixin

class AuditLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._start_time = time.time()

    def process_response(self, request, response):
        duration = time.time() - getattr(request, "_start_time", time.time())
        if duration > 3:
            print(f"[AUDIT] Slow request {request.path} ({duration}s)")
        return response
