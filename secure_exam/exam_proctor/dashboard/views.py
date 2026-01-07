from django.shortcuts import render
from exam_proctor.models import ProctorViolation

def dashboard(request):
    violations = ProctorViolation.objects.order_by("-created_at")[:100]
    return render(request, "dashboard/index.html", {
        "violations": violations
    })
