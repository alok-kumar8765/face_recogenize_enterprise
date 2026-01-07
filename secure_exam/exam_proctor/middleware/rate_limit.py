from django.http import JsonResponse

class HardRateLimit:
    def __init__(self, get_response):
        self.get_response = get_response
        self.hits = {}

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        self.hits[ip] = self.hits.get(ip, 0) + 1
        if self.hits[ip] > 200:
            return JsonResponse({"error": "Too many requests"}, status=429)
        return self.get_response(request)

from django.http import JsonResponse
import time

REQUEST_LIMIT = 100
WINDOW = 60  # seconds

class RateLimitMiddleware:
    clients = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        now = time.time()

        hits = self.clients.get(ip, [])
        hits = [t for t in hits if now - t < WINDOW]
        hits.append(now)
        self.clients[ip] = hits

        if len(hits) > REQUEST_LIMIT:
            return JsonResponse({"error": "Rate limit exceeded"}, status=429)

        return self.get_response(request)
