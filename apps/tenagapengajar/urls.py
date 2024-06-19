from django.urls import path, re_path
from django.views.generic import TemplateView
from aplikasi_manajemen_penjadwalan.views import JadwalListView
from .views import (
    JadwalCreateView,
    JadwalUpdateView,
    JadwalDeleteView,
    RevisiJadwalListView
)


app_name = 'tenagapengajar'
urlpatterns = [
    path('jadwal/tambah/', JadwalCreateView.as_view(), name='jadwal_create'),
    path('jadwal/revisi_list/', RevisiJadwalListView.as_view(),
         name='perbaiki_revisi_jadwal'),
    path('jadwal/update/<int:pk>/',
         JadwalUpdateView.as_view(), name='jadwal_update'),
    path('jadwal/delete/<int:pk>/',
         JadwalDeleteView.as_view(), name='jadwal_delete'),
]
# add a flag for handling 404 page not found error
handler404 = 'aplikasi_manajemen_penjadwalan.views.error_404_view'
