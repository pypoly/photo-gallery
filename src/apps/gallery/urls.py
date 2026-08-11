from django.contrib import admin
from django.urls import path
from . import views
from apps import gallery
from apps.gallery.views import PhotoListView, PhotoCreateView, PhotoUpdateView, PhotoDeleteView, PhotoDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PhotoListView.as_view(), name = 'gallery'),
    path('photo', PhotoCreateView.as_view(), name = 'add_photo'),
    path('photo/edit/<int:pk>', PhotoUpdateView.as_view(), name = 'update_photo'),
    path('photo/delete/<int:pk>', PhotoDeleteView.as_view(), name = 'delete_photo'),
    path('photo/<int:pk>', PhotoDetailView.as_view(), name = 'photo'),
]
