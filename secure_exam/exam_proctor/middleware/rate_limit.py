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
