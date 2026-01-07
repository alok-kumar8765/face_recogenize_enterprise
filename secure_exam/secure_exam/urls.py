from django.urls import path, include

urlpatterns = [
    path('exam/', include('exam.urls')),
]
