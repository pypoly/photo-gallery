import os

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, Http404
from django.urls import reverse
from django.views.generic import ListView, UpdateView, DetailView, CreateView, DeleteView

from apps.gallery.forms import UpdatePhotoForm, PhotoCreateForm, AlbumCreateForm, AlbumUpdateForm, PhotoFilterForm, UserRegisterForm
from apps.gallery.models import Photo, Album
from .tasks import create_thumbnail
# список фото

class PhotoListView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'gallery/photo_list.html'
    paginate_by = 18


    def get_queryset(self):
        qs = Photo.objects.filter(user=self.request.user)
        # Создание формы фильтрации
        self.filter_form = PhotoFilterForm(data=self.request.GET)
        if self.filter_form.is_valid():
            from_date = self.filter_form.cleaned_data.get('from_date')
            to_date = self.filter_form.cleaned_data.get('to_date')
            if from_date:
                qs = qs.filter(created_at__gte=from_date)
            if to_date:
                qs = qs.filter(created_at__lte=to_date)
        return qs

    def get_context_data(self, *args, **kwargs):
        """
        Добавляем форму фильтрации в контекст
        """
        ctx = super().get_context_data(*args, **kwargs)
        ctx['filter_form'] = self.filter_form
        return ctx

# детали одного фото
class PhotoDetailView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'gallery/photo_detail.html'

    def get(self, request, *args, **kwargs):
        photo = self.get_object()
        if photo.user != self.request.user:
            raise Http404
        return super().get(request, *args, **kwargs)

# создание фото
class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoCreateForm
    template_name = 'gallery/photo_create.html'

    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        form.fields['album'].queryset = Album.objects.filter(user=self.request.user)
        return form

    def get_success_url(self):
        return reverse('gallery:photo', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        create_thumbnail.delay(form.instance.id)
        return response

    # данные по умолчанию для формы создания фотки
    def get_initial(self):
        initial = super().get_initial()

        album_id = self.request.GET.get('to')
        if album_id:
            initial['album'] = album_id
        return initial

# редактирование фото
class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    template_name = 'gallery/photo_update.html'
    form_class =  UpdatePhotoForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['album'].queryset = Album.objects.filter(user=self.request.user)
        return form

    def dispatch(self, request, *args, **kwargs):
        photo = self.get_object()
        if photo.user != self.request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('gallery:photo', kwargs={'pk': self.object.id})


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


# =====================================================================================================================

class AlbumListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'gallery/album_list.html'
    queryset = Album.objects.filter(private=False)
    paginate_by = 8

    def get_queryset(self):
        return Album.objects.filter(user=self.request.user)

class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumCreateForm
    template_name = 'gallery/album_create.html'

    def get_success_url(self):
        return reverse('gallery:album_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # def get(self, request, *args, **kwargs):
    #     photo = self.get_object()
    #     if photo.user != self.request.user:
    #         raise Http404
    #     return super().get(request, *args, **kwargs)


class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'gallery/album_detail.html'


class AlbumUpdateView(LoginRequiredMixin, UpdateView):
    model = Album
    form_class = AlbumUpdateForm
    template_name = 'gallery/album_update.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        photo = self.get_object()
        if photo.user != self.request.user:
            raise Http404
        return super().get(request, *args, **kwargs)

class AlbumDeleteView(LoginRequiredMixin, DeleteView):
    model = Album
    template_name = 'gallery/album_delete.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.thumbnail:
            path = obj.thumbnail.path
            if os.path.exists(path):
                os.unlink(path)
        return super().post(request, *args, **kwargs)

# ============================================================================
class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'gallery/registration.html'
    success_url = '/'

    def get(self, request: HttpRequest, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('gallery:index')
        return super().get(request, *args, **kwargs)

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'gallery/profile.html'
