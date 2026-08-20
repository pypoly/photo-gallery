from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import LogoutView, LoginView
from django.views.generic.base import TemplateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from apps.gallery.views import UserRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration', UserRegisterView.as_view(), name='registration'),
    path('login', LoginView.as_view(template_name='gallery/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    # path('profile', UserProfileView.as_view(), name='profile'),
    path('profile', PasswordChangeView.as_view(
        template_name='gallery/profile.html',
        success_url=reverse_lazy("gallery:index"),
        # form_class=PasswordChangeForm
    ), name='profile'),
    path('', include('apps.gallery.urls', namespace='gallery')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
