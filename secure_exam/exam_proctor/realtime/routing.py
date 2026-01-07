from django.urls import re_path
from .consumers import ProctorFeed

websocket_urlpatterns = [
    re_path(r'ws/proctor/$', ProctorFeed.as_asgi()),
]
