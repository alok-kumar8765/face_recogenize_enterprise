# 🎥 Django Exam Proctoring System (AI + Anti-Cheat)

A **production-grade, AI-powered exam proctoring system** built with Django.
Designed for **online exams, certifications, hiring tests, and remote assessments**.

Supports:
- Face verification
- Liveness detection (blink, head movement)
- Anti-cheating (tab switch, camera off, noise detection)
- Evidence storage
- SaaS-ready API
- Open-source friendly

---

## 🚀 Features

### ✅ Identity Verification
- Face match (candidate vs registered image)
- Multiple face detection
- Auto failure on mismatch

### 👁️ Liveness Detection
- Eye blink detection
- Head movement (left-right)
- Spoof prevention

### 🔐 Anti-Cheating
- Tab switch detection
- Camera disabled detection
- Noise / talking detection
- Rate limiting
- Session violation tracking

### 📦 Enterprise Ready
- REST APIs (JSON)
- JWT authentication
- API key authentication
- Evidence storage
- Audit logs
- Docker & Kubernetes ready

---

## 🏗️ Architecture

```

secure_exam/
│
├── exam_proctor/ ← Reusable Django App
│ ├── anti_cheat/
│ ├── liveness/
│ ├── views/
│ ├── evidence/
│ ├── middleware/
│ ├── billing/
│ └── api/
│
└── manage.py
```

---


## 📥 Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/alok-kumar8765/face_recogenize_enterprise.git
cd face_recogenize_enterprise
```

## 2️⃣ Create Virtual Environment

```
python -m venv venv
source venv/bin/activate
```

## 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

## ⚙️ Django Setup
Add App

```

# settings.py
INSTALLED_APPS = [
    ...
    'exam_proctor',
]
```

Add Middleware

```
MIDDLEWARE += [
    'exam_proctor.middleware.rate_limit.RateLimitMiddleware',
    'exam_proctor.middleware.audit_log.AuditLogMiddleware',
]
```

Media Settings

```
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

```

---

## ▶️ Run Server

```
python manage.py migrate
python manage.py runserver
```

---

## 🧪 Usage (Basic)
Face + Liveness Verification

```
POST /exam/secure/
Content-Type: application/json

{
  "reg_id": "CAND123",
  "image": "data:image/jpeg;base64,...",
  "state": {}
}
```

---

Response

```
{
  "step": "face",
  "face_match": true,
  "message": "Face + Liveness Verified"
}
```

---

## 🔐 Security

- CSRF exempted APIs

- JWT authentication

- API-key based SaaS access

- Rate limited endpoints

---

## 🧩 Extending

You can:

- Plug into LMS

- Use as SaaS API

- Deploy on Kubernetes

- White-label UI

- Add payment gateway

---

## 🧠 Who Should Use This?

- EdTech platforms

-Online exam providers

- Hiring & assessment companies

- Certification authorities

- Universities

---

## 📜 License

| MIT License – Free for commercial & personal use.

---

## ⭐ Contribute

Pull requests welcome.
Issues & feature requests encouraged.

---

## ❤️ Built With

-Django

-OpenCV

-MediaPipe

-NumPy

-Redis

```

---

# PART 2️⃣ — **SaaS API Authentication**

Now we add **real SaaS-level auth**.

---

## 🔑 OPTION A — API KEY AUTH (For SaaS clients)

### 📁 `api/models.py`

```python
from django.db import models
import uuid

class APIClient(models.Model):
    name = models.CharField(max_length=100)
    api_key = models.UUIDField(default=uuid.uuid4, unique=True)
    is_active = models.BooleanField(default=True)
```

---


## 📁 api/auth.py

```
from django.http import JsonResponse
from .models import APIClient

def api_key_required(view_func):
    def wrapper(request, *args, **kwargs):
        key = request.headers.get("X-API-KEY")
        if not key:
            return JsonResponse({"error": "API key missing"}, status=401)

        try:
            client = APIClient.objects.get(api_key=key, is_active=True)
            request.api_client = client
        except APIClient.DoesNotExist:
            return JsonResponse({"error": "Invalid API key"}, status=403)

        return view_func(request, *args, **kwargs)
    return wrapper
```

---

## ✅ Protect Any API

```

from exam_proctor.api.auth import api_key_required

@api_key_required
def face_only_verify(request):
    ...
```

---

## 🔐 JWT AUTH (For Web / Mobile)
📦 Install

```
pip install djangorestframework-simplejwt
```

---

## ⚙️ settings.py

```

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

---

## 📁 api/views.py

```
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def secure_exam_api(request):
    return Response({"status": "Authorized"})
```

---

## 🔑 Token Endpoint

```
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns += [
    path("api/token/", TokenObtainPairView.as_view()),
]
```

---

## 🧠 Auth Strategy (REAL WORLD)

| Use Case       | Auth    |
| -------------- | ------- |
| SaaS Clients   | API Key |
| Web Exams      | JWT     |
| Mobile Apps    | JWT     |
| Internal Admin | Session |

---








































