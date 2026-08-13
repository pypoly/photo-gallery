from django.contrib import admin
from django.urls import path
from . import views
from apps import gallery
from apps.gallery.views import PhotoListView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView, PhotoDetailView, \
    AlbumListView, AlbumCreateView, AlbumUpdateView, AlbumDeleteView, AlbumDetailView

urlpatterns = [
    path('', PhotoListView.as_view(), name = 'gallery'),
    path('photo', PhotoCreateView.as_view(), name = 'add_photo'),
    path('photo/edit/<int:pk>', PhotoUpdateView.as_view(), name = 'update_photo'),
    path('photo/delete/<int:pk>', PhotoDeleteView.as_view(), name = 'delete_photo'),
    path('photo/<int:pk>', PhotoDetailView.as_view(), name = 'photo'),
    path('albums/', AlbumListView.as_view(), name = 'album_list'),
    path('albums/create/<int:pk>', AlbumCreateView.as_view(), name = 'add_album'),
    path('albums/edit/<int:pk>', AlbumUpdateView.as_view(), name = 'update_album'),
    path('albums/delete/<int:pk>', AlbumDeleteView.as_view(), name = 'delete_album'),
    path('albums/<int:pk>', AlbumDetailView.as_view(), name = 'detail_album'),
]
