from django.urls import path, re_path
from django.views.generic import TemplateView

from administrator.reset_views import kelas_peserta_reset

from .views import (
    IndexView,
    GuruListView,
    GuruCreateView,
    GuruUpdateView,
    GuruDeleteView,
    MataPelajaranIndexView,
    MataPelajaranCreateView,
    MataPelajaranUpdateView,
    MataPelajaranDeleteView,
    DetailMataPelajaranIndexView,
    DetailMataPelajaranCreateView,
    DetailMataPelajaranUpdateView,
    DetailMataPelajaranDeleteView,
    RuanganListView,
    RuanganCreateView,
    RuanganUpdateView,
    RuanganDeleteView,
    DetailKelasCreateView,
    DetailKelasUpdateView,
    DetailKelasDeleteView,
    KelasIndexView,
    WaktuIndexView,
    WaktuCreateView,
    WaktuUpdateView,
    WaktuDeleteView,
    DetailWaktuCreateView,
    DetailWaktuUpdateView,
    DetailWaktuDeleteView,
    ResetIndexView,
    guru_reset,
    mata_pelajaran_reset,
    ruangan_reset,
    waktu_reset,
    detail_mata_pelajaran_reset,
    detail_waktu_reset,
    jadwal_reset,
    search_detail_pelajaran,
    search_guru,
    search_detail_waktu,
    search_ruangan,
    search_mapel,
    search_kelas_peserta
)

app_name = 'administrator_IT'
urlpatterns = [
    path('guru/', GuruListView.as_view(), name='guru_list'),
    path('guru/tambah/', GuruCreateView.as_view(), name='guru_create'),
    path('guru/update/<int:pk>/', GuruUpdateView.as_view(), name='guru_update'),
    path('guru/delete/<int:pk>/', GuruDeleteView.as_view(), name='guru_delete'),

    path('mata_pelajaran/', MataPelajaranIndexView.as_view(),
         name='mata_pelajaran_list'),
    path('mata_pelajaran/tambah/', MataPelajaranCreateView.as_view(),
         name='mata_pelajaran_create'),
    path('mata_pelajaran/update/<int:pk>/',
         MataPelajaranUpdateView.as_view(), name='mata_pelajaran_update'),
    path('mata_pelajaran/delete/<int:pk>/',
         MataPelajaranDeleteView.as_view(), name='mata_pelajaran_delete'),

    path('detail_mata_pelajaran/', DetailMataPelajaranIndexView.as_view(),
         name='detail_mata_pelajaran_list'),
    path('detail_mata_pelajaran/tambah/', DetailMataPelajaranCreateView.as_view(),
         name='detail_mata_pelajaran_create'),
    path('detail_mata_pelajaran/update/<int:pk>/',
         DetailMataPelajaranUpdateView.as_view(), name='detail_mata_pelajaran_update'),
    path('detail_mata_pelajaran/delete/<int:pk>/',
         DetailMataPelajaranDeleteView.as_view(), name='detail_mata_pelajaran_delete'),

    path('ruangan/', RuanganListView.as_view(), name='ruangan_list'),
    path('ruangan/tambah/', RuanganCreateView.as_view(), name='ruangan_create'),
    path('ruangan/update/<int:pk>/',
         RuanganUpdateView.as_view(), name='ruangan_update'),
    path('ruangan/delete/<int:pk>/',
         RuanganDeleteView.as_view(), name='ruangan_delete'),

    path('kelas/', KelasIndexView.as_view(), name='kelas_list'),
    path('kelas/tambah/', DetailKelasCreateView.as_view(), name='kelas_create'),
    path('kelas/update/<int:pk>/',
         DetailKelasUpdateView.as_view(), name='kelas_update'),
    path('kelas/delete/<int:pk>/',
         DetailKelasDeleteView.as_view(), name='kelas_delete'),

    path('waktu/', WaktuIndexView.as_view(),
         name='waktu_list'),
    path('waktu/tambah/', WaktuCreateView.as_view(),
         name='waktu_create'),
    path('waktu/update/<int:pk>/',
         WaktuUpdateView.as_view(), name='waktu_update'),
    path('waktu/delete/<int:pk>/',
         WaktuDeleteView.as_view(), name='waktu_delete'),

    path('detail_waktu/tambah/', DetailWaktuCreateView.as_view(),
         name='detail_waktu_create'),
    path('detail_waktu/update/<int:pk>/',
         DetailWaktuUpdateView.as_view(), name='detail_waktu_update'),
    path('detail_waktu/delete/<int:pk>/',
         DetailWaktuDeleteView.as_view(), name='detail_waktu_delete'),

    path('reset/',
         ResetIndexView.as_view(), name='reset_index'),
    path('reset/jadwal',
         jadwal_reset, name='jadwal_reset'),
    path('reset/guru',
         guru_reset, name='guru_reset'),
    path('reset/mata_pelajaran',
         mata_pelajaran_reset, name='mata_pelajaran_reset'),
    path('reset/kelas_peserta',
         kelas_peserta_reset, name='kelas_peserta_reset'),
    path('reset/ruangan',
         ruangan_reset, name='ruangan_reset'),
    path('reset/waktu',
         waktu_reset, name='waktu_reset'),
    path('reset/detail_mata_pelajaran',
         detail_mata_pelajaran_reset, name='detail_mata_pelajaran_reset'),
    path('reset/detail_waktu',
         detail_waktu_reset, name='detail_waktu_reset'),

    path('search_detail_pelajaran/', search_detail_pelajaran,
         name='search_detail_pelajaran'),
    path('search_guru/', search_guru, name='search_guru'),
    path('search_detail_waktu/', search_detail_waktu, name='search_detail_waktu'),
    path('search_ruangan/', search_ruangan, name='search_ruangan'),
    path('search_mapel/', search_mapel, name='search_mapel'),
    path('search_kelas_peserta/', search_kelas_peserta,
         name='search_kelas_peserta'),

    path('', IndexView.as_view(), name='index'),
]
# add a flag for handling 404 page not found error
handler404 = 'aplikasi_manajemen_penjadwalan.views.error_404_view'