from django.urls import path, re_path
from .views import profile, ChangePasswordView, UserProfileIndexView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'users'
urlpatterns = [
    path('profile/', UserProfileIndexView.as_view(), name='profile'),
    path('edit_profile/', profile, name='edit_profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
# else:
#     urlpatterns += staticfiles_urlpatterns()
# add a flag for handling 404 page not found error
handler404 = 'aplikasi_manajemen_penjadwalan.views.error_404_view'
