# exam_proctor/middleware.py

from django.http import JsonResponse
from exam_proctor.models import Institute
import redis
from django.http import JsonResponse


class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        api_key = request.headers.get('X-API-KEY')
        if not api_key:
            return JsonResponse({'error': 'API key required'}, status=401)
        try:
            request.institute = Institute.objects.get(api_key=api_key)
        except Institute.DoesNotExist:
            return JsonResponse({'error': 'Invalid API key'}, status=403)
        return self.get_response(request)

# exam_proctor/middleware.py
r = redis.Redis(host='localhost', port=6379, db=0)

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        key = f"rl:{request.institute.id}:{request.path}"
        count = r.get(key)
        if count and int(count) > 50:
            return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
        r.incr(key, 1)
        r.expire(key, 60)  # 1 minute
        return self.get_response(request)
