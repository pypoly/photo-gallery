from django.contrib import admin

from apps.gallery.models import Photo, Album

admin.site.register(Photo)
admin.site.register(Album)

