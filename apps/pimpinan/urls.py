from django.urls import path, include
from .views import (
    RevisiJadwalListView,
    RevisiJadwalUpdateView,
    RevisiJadwalDeleteView,
    RevisiJadwalCreateView,
    lock_jadwal,
    unlock_specific_jadwal,
    validasi_all_jadwal
)

app_name = 'pimpinan'
urlpatterns = [
    path('revisi_jadwal/', RevisiJadwalListView.as_view(),
         name='revisi_jadwal_list'),
    path('revisi_jadwal/tambah/<int:pk>/', RevisiJadwalCreateView.as_view(),
         name='revisi_jadwal_create'),
    path('revisi_jadwal/update/<int:pk>/',
         RevisiJadwalUpdateView.as_view(), name='revisi_jadwal_update'),
    path('revisi_jadwal/delete/<int:pk>/',
         RevisiJadwalDeleteView.as_view(), name='revisi_jadwal_delete'),
    path('lock_jadwal/<int:pk>/',
         lock_jadwal, name='lock_specific_jadwal'),
    path('validasi_jadwal/<str:status_validasi>/',
         validasi_all_jadwal, name='validasi_jadwal'),
    path('unlock_jadwal/<int:pk>/',
         unlock_specific_jadwal, name='unlock_specific_jadwal'),
]

# # add a flag for handling 404 page not found error
handler404 = 'aplikasi_manajemen_penjadwalan.views.error_404_view'
