import io
import math
import random

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from PIL import Image

from apps.gallery.forms import AlbumCreateForm
from apps.gallery.models import Photo


class Command(BaseCommand):
    help = "Seed database with users, albums and photos"

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, required=True, help='Number of users to create')
        parser.add_argument('--photos-per-user', type=int, required=True, dest='photos_per_user', help='Number of photos per user')

    def handle(self, *args, **options):
        num_users = options['users']
        photos_per_user = options['photos_per_user']

        fake = Faker()

        # Create dummy image once
        dummy_img = Image.new('RGB', (2, 2), color=(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        ))
        buf = io.BytesIO()
        dummy_img.save(buf, format='JPEG')
        dummy_content = buf.getvalue()

        for user_idx in range(num_users):
            username = f'seed_user_{user_idx + 1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'is_active': True},
            )
            if created:
                user.set_password('password')
                user.save()

            self.stdout.write(f'[{user_idx + 1}/{num_users}] Created user {username}')
            num_albums = math.ceil(photos_per_user / 100.0) if photos_per_user > 0 else 0
            if num_albums == 0:
                continue

            albums = []
            for album_idx in range(num_albums):
                uploaded = SimpleUploadedFile(
                    f'seed_{random.randint(100000, 999999)}.jpg',
                    dummy_content,
                    content_type='image/jpeg',
                )

                form = AlbumCreateForm(
                    data={'name': fake.company()},
                    files={'thumbnail': uploaded},
                )
                form.instance.user = user
                if form.is_valid():
                    album = form.save()
                    albums.append(album)
                else:
                    form = AlbumCreateForm(data={'name': fake.company()}, files={})
                    form.instance.user = user
                    album = form.save()
                    albums.append(album)
                self.stdout.write(f'  -> album {album_idx + 1}/{num_albums}')

            if not albums:
                continue

            photos_created = 0
            album_idx = 0
            batch = []
            batch_size = 100
            while photos_created < photos_per_user:
                album = albums[album_idx % len(albums)]
                filename = f'seed_{random.randint(100000, 999999)}.jpg'
                uploaded = SimpleUploadedFile(
                    filename,
                    dummy_content,
                    content_type='image/jpeg',
                )

                photo = Photo(user=user, album=album)
                photo.image.save(filename, uploaded, save=False)
                batch.append(photo)
                photos_created += 1
                album_idx += 1

                if len(batch) >= batch_size:
                    Photo.objects.bulk_create(batch)
                    batch = []
                    self.stdout.write(f'    photo {photos_created}/{photos_per_user}')

            if batch:
                Photo.objects.bulk_create(batch)
                self.stdout.write(f'    photo {photos_created}/{photos_per_user}')
            self.stdout.write(self.style.SUCCESS(f'User {username} done'))
