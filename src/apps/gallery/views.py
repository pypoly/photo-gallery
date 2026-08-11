import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import ListView, UpdateView, DetailView, CreateView, DeleteView

from apps.gallery.forms import UpdatePhotoForm, PhotoForm, PhotoCreateForm
from apps.gallery.models import Photo, Album

# список фото
class PhotoListView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'gallery/photo_list.html'

# детали одного фото
class PhotoDetailView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'gallery/photo_detail.html'

# создание фото
class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoCreateForm
    template_name = 'gallery/photo_create.html'

    def get_success_url(self):
        return reverse('photo', kwargs={'pk': self.object.id})


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# редактирование фото
class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    template_name = 'gallery/photo_update.html'
    form_class =  UpdatePhotoForm

    def get_success_url(self):
        return reverse('photo', kwargs={'pk': self.object.id})


# удаление фото
class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    template_name = 'gallery/photo_delete.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        path = self.get_object().image.path
        if os.path.exists(path):
           os.unlink(path)
        return super().post(request, *args, **kwargs)


# =====================================

class AlbumListView(ListView):
    model = Album
    template_name = 'gallery/album_list.html'
    queryset = Album.objects.filter(private=False)

