import os
from django.core.files.base import ContentFile
from django.conf import settings
import base64
import uuid

def save_evidence(base64_file, file_type="png"):
    data = base64.b64decode(base64_file.split(",")[1])
    name = f"{uuid.uuid4()}.{file_type}"

    path = os.path.join(settings.MEDIA_ROOT, "evidence", name)

    with open(path, "wb") as f:
        f.write(data)

    return f"evidence/{name}"
