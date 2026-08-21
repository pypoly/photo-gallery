from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import Form

from apps.gallery.models import Photo, Album


class PhotoCreateForm(forms.ModelForm):
    # album = forms.ModelChoiceField(queryset=Album.objects.none())
    # user = forms.ModelChoiceField(blank=True, queryset=User.objects.all())

    class Meta:
        model = Photo
        fields = ('image', 'album')#, 'user')
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control rounded-3'}),
            'album': forms.Select(attrs={'class': 'form-select rounded-3'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['album'].required = True
        self.fields['album'].queryset = Album.objects.filter(private=False)

class UpdatePhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('thumbnail', 'created_at', 'image', 'album')
        widgets = {
            'created_at': forms.DateTimeInput(
                attrs={'class': 'form-control rounded-end-3', 'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ'},
                format='%Y-%m-%d %H:%M',
            ),
            'album': forms.Select(attrs={'class': 'form-select rounded-3'}),
        }


# =================================================================================

class AlbumCreateForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('name', 'private', 'thumbnail')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control rounded-3', 'placeholder': 'Например, Отпуск 2026'}),
            'private': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }


class AlbumUpdateForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('thumbnail', 'name', 'private')
        widgets = {
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control rounded-3'}),
            'name': forms.TextInput(attrs={'class': 'form-control rounded-3'}),
            'private': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control rounded-end-3',
                'placeholder': 'Введите имя пользователя',
                'autocomplete': 'username',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control rounded-end-3',
            'placeholder': 'Введите пароль',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control rounded-end-3',
            'placeholder': 'Повторите пароль',
            'autocomplete': 'new-password',
        })


class PhotoFilterForm(Form):
    from_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control rounded-3', 'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M',
        ),
    )
    to_date = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control rounded-3', 'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M',
        ),
    )

