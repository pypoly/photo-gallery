from django import forms

from apps.gallery.models import Photo, Album

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', 'name')

class UpdatePhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('thumbnail', 'uploaded_at')

class UpdateAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('thumbnail', 'name', 'private')
    