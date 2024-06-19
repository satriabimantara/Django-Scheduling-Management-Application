from django.db import models
from tenagapengajar.models import Jadwal
# Create your models here.


class RevisiJadwal(models.Model):
    jadwal = models.OneToOneField(
        Jadwal,
        on_delete=models.CASCADE,
        primary_key=True
    )
    revisi_messages = models.TextField(
        "Pesan Revisi untuk Jadwal",
        max_length=500
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
        ordering = ['updated']
        verbose_name_plural = "Revisi Jadwal"

    def __str__(self):
        return "[{}]. {}".format(self.updated, self.jadwal)
