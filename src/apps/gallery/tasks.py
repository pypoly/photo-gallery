from PIL import Image
from celery import Celery
from django.tasks import task

from apps.gallery.models import Photo
from main.celery import app


@app.task
def create_thumbnail(photo_id: int):
    photo = Photo.objects.get(pk=photo_id)
    image_path = photo.image.path
    # get photo date from exif
    img = Image.open(image_path).convert('RGB')
    img.save(image_path, quality=90)
    img.thumbnail((250, 250), Image.Resampling.LANCZOS)

    form = PhotoUpdate(
        data={'created_at': ''},
        files={'thumbnail': img},
    )
    if form.is_valid():
        form.save()

