from django import forms

from apps.gallery.models import Photo, Album

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image',)

class UpdatePhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('thumbnail', 'created_at')
        widgets = {
            'created_at': forms.DateTimeInput(
                attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ'},
                format='%Y-%m-%d %H:%M',
            ),
        }

class UpdateAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('thumbnail', 'name', 'private')

class PhotoCreateForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image',)
