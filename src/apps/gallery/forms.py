from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

from apps.gallery.models import Photo, Album


class PhotoCreateForm(forms.ModelForm):
    # album = forms.ModelChoiceField(queryset=Album.objects.none())

    class Meta:
        model = Photo
        fields = ('image', 'album')
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'album': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['album'].required = True
        self.fields['album'].queryset = Album.objects.filter(private=False)

class UpdatePhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('thumbnail', 'created_at', 'image')
        widgets = {
            'created_at': forms.DateTimeInput(
                attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ'},
                format='%Y-%m-%d %H:%M',
            ),
        }


# =================================================================================

class AlbumCreateForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('name', 'private')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например, Отпуск 2026'}),
            'private': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }


class AlbumUpdateForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('thumbnail', 'name', 'private')
        widgets = {
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'private': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }


#
# class UserRegisterForm(UserCreationForm):
#     class Meta:
#         model = User
#         email = forms.EmailField()
#         password = forms.CharField()
