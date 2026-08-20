from django.contrib import admin

from apps.gallery.models import Photo, Album

admin.site.register(Photo)
@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_filter = ('user',)


