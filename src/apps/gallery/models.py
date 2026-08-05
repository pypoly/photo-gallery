import os
import secrets
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



def get_upload_photo_path(instance, filename):
    base, ext = os.path.splitext(filename)
    return os.path.join(
        'photos',
        str(instance.user.id),
        base+f'_{secrets.token_urlsafe(8)}'+ext
    )


def get_upload_thumbnail_path(instance: Photo, filename):
    rel = os.path.relpath(instance.image.path, start=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(rel)
    return f'{base}-thumbnail{ext}'


class Photo(models.Model):
    image = models.FileField(upload_to=get_upload_photo_path)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to=get_upload_thumbnail_path, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    album = models.ForeignKey('gallery.Album', on_delete=models.RESTRICT)

def get_album_path(instance, filename):
    base, ext = os.path.splitext(filename)
    return os.path.join(
        'albums',
        base + f'_{secrets.token_urlsafe(8)}' + ext
    )

class Album(models.Model):
    name = models.CharField(max_length=100)
    # photos = ManyToManyField(Photo)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to=get_album_path, null=True)







