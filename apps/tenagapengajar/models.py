from django.db import models
from administrator.models import (
    DetailMataPelajaran,
    Guru,
    DetailWaktu,
    Ruangan
)
# Create your models here.


class Jadwal(models.Model):
    detail_pelajaran = models.ForeignKey(
        DetailMataPelajaran,
        on_delete=models.CASCADE
    )
    guru = models.ForeignKey(
        Guru,
        on_delete=models.CASCADE,
        default='- Belum Ada Pengajar -',
        blank=True,
        null=False
    )
    detail_waktu = models.ForeignKey(
        DetailWaktu,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    ruangan = models.ForeignKey(
        Ruangan,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    CHOICE_STATUS_VALIDASI = (
        ('Unlock', 'Unlock'),
        ('Lock', 'Lock'),
    )
    status_validasi = models.CharField(
        'Status Validasi Jadwal',
        choices=CHOICE_STATUS_VALIDASI,
        default=CHOICE_STATUS_VALIDASI[0][1],
        max_length=10,
    )
    published = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False
    )

    class Meta:
        ordering = ['published']
        verbose_name_plural = "Jadwal"

    def __str__(self):
        final_string = "{}. {} - {} - {} - {} | ".format(
            self.id,
            self.detail_pelajaran.mapel.mapel,
            self.guru.nama_lengkap,
            self.detail_pelajaran.kelas_peserta.kelas,
            self.detail_pelajaran.kelas_peserta.jalur.nama_jalur
        )
        # cek apakah waktu None?
        if self.detail_waktu == None:
            extra_string = "-- WITA | "
        else:
            extra_string = "{}: {} | ".format(
                self.detail_waktu.hari.nama_hari,
                self.detail_waktu.waktu.nama_waktu
            )
        final_string += extra_string
        # cek apakah ruangan None?
        if self.ruangan == None:
            extra_string = "- ruang | "
        else:
            extra_string = "{}".format(
                self.ruangan.nama_ruangan,
            )
        final_string += extra_string
        return final_string
