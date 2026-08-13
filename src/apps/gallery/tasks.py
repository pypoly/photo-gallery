import os
from datetime import datetime
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from celery import Celery
from django.core.files.uploadedfile import UploadedFile
from django.tasks import task

from apps.gallery.forms import UpdatePhotoForm
from apps.gallery.models import Photo
from main.celery import app


@app.task
def create_thumbnail(photo_id: int):
    # photo_id = 16
    photo = Photo.objects.get(pk=photo_id)
    image_path = photo.image.path
    if not os.path.exists(image_path):
        return

    rgb_img = to_jpg(photo.image.path)
    thumbnail = rgb_img.copy()
    thumbnail.thumbnail((250, 250), Image.Resampling.LANCZOS)
    creation_date = get_creation_date(image_path)

    data = {}
    if creation_date:
        data['created_at'] = creation_date
    file_base_name = os.path.splitext(os.path.basename(image_path))[0]
    files = {
        'image': to_content_file(rgb_img, file_base_name+'.jpg'),
        'thumbnail': to_content_file(thumbnail, file_base_name+'_thumbnail.jpg'),
    }
    form = UpdatePhotoForm(
        instance=photo,
        data=data,
        files=files,
    )
    if form.is_valid():
        form.save()
        photo.refresh_from_db()
        if photo.image.path != image_path:
            os.remove(image_path)


def to_jpg(path):
    img = Image.open(path)
    name, ext = os.path.splitext(path)
    if ext.strip('.').lower() != 'jpg':
        img = img.convert('RGB')
    return img


def get_creation_date(path) -> datetime:
    return datetime.now()


def to_content_file(img: Image.Image, name) -> ContentFile:
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=85, optimize=True)  # quality от 1 до 100
    buffer.seek(0)
    return ContentFile(buffer.read(), name)

