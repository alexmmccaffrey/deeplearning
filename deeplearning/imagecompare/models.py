import os
from django.conf import settings
from django.db import models
from uuid import uuid4

class Image(models.Model):
    def set_path_and_filename(instance, filename):
        path = settings.MEDIA_ROOT
        filename = f'{uuid4().hex}{os.path.splitext(filename)[1]}'
        path_and_filename = os.path.join(path, filename)
        return path_and_filename

    path = set_path_and_filename
    image = models.ImageField(upload_to=path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

