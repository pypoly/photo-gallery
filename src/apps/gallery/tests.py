import io

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.test import TestCase

from apps.gallery.models import Album, Photo
from apps.gallery.tasks import create_thumbnail
from main.celery import app as celery_app


def make_image_file(name='test.png', color='red'):
    from PIL import Image
    buffer = io.BytesIO()
    Image.new('RGB', (300, 300), color).save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name)


class PhotoAlbumTestCase(TestCase):
    def setUp(self):
        celery_app.conf.task_always_eager = True
        self.user = User.objects.create_user(username='tester', password='pass12345')
        self.client.force_login(self.user)
        self.album = Album.objects.create(name='Отпуск', user=self.user)

    def test_photo_created_via_album_keeps_album_after_thumbnail_task(self):
        response = self.client.post(
            '/photo',
            {'image': make_image_file(), 'album': self.album.pk},
        )
        self.assertEqual(response.status_code, 302)
        photo = Photo.objects.get(user=self.user)
        photo.refresh_from_db()
        self.assertEqual(photo.album, self.album)
        self.assertIsNotNone(photo.thumbnail)

    def test_create_thumbnail_task_does_not_touch_album(self):
        photo = Photo(user=self.user, album=self.album)
        photo.image.save('raw.png', make_image_file(color='green'), save=True)

        create_thumbnail.apply(args=[photo.pk], throw=True)

        photo.refresh_from_db()
        self.assertEqual(photo.album, self.album)
        self.assertEqual(photo.user, self.user)
        self.assertIsNotNone(photo.thumbnail)
