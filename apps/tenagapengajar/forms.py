from django import forms
from .models import Jadwal
from django.core.exceptions import ValidationError
from pimpinan.models import RevisiJadwal


class JadwalForm(forms.ModelForm):
    class Meta:
        model = Jadwal
        fields = [
            'detail_pelajaran',
            'guru',
            'detail_waktu',
            'ruangan'
        ]
        widgets = {
            'detail_pelajaran': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': 'True'
                }
            ),
            'guru': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': 'True'
                }
            ),
            'detail_waktu': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': 'True'
                }
            ),
            'ruangan': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': 'True'
                }
            ),
        }

    def check_if_revisi_jadwal_exist_with_this_updated_jadwal(self, **kwargs):
        # check apakah ada id_jadwal di tabel RevisiJadwal
        revised_jadwal = RevisiJadwal.objects.filter(
            jadwal__id=kwargs['id']
        )
        if revised_jadwal.count() > 0:
            return revised_jadwal.count(), revised_jadwal
        else:
            return 0, []

    def clean(self, *args, **kwargs):
        # method ini akan dipanggil sebelum is_valid() form dijalankan
        cleaned_data = super().clean(*args, **kwargs)
        detail_pelajaran = cleaned_data.get('detail_pelajaran')
        detail_waktu = cleaned_data.get('detail_waktu')
        guru = cleaned_data.get('guru')
        ruangan = cleaned_data.get('ruangan')

        """
        CHECK CONSTRAINT JADWAL TERBENTUR
        ================================
        1. Check apakah data jadwal yang sama sudah ada di database?
        2. Check apakah di jam yang sama, suatu kelas yang sama sudah ada jadwal yang diplot?
        3. Check apakah di jam yang sama, suatu ruangan yang sama menerima jadwal pelajaran yang berbeda?
        4. Check apakah di jam yang sama, suatu guru yang sama mengajar lebih dari satu jadwal pelajaran yang berbeda?
        5. Check apakah suatu kelas dijadwalkan melebihi jam pelajaran yang semestinya? Misal kelas X-Umum seharusnya menerima 3 jam mata pelajaran, namun dijadwalkan untuk 4 jam mata pelajaran
        """

        # buat variable untuk menampung seluruh pesan error yang muncul
        validation_error_messages = dict()

        # check apakah data jadwal persis sudah ada di database?
        existing = Jadwal.objects.filter(
            detail_pelajaran=detail_pelajaran,
            detail_waktu=detail_waktu,
            guru=guru,
            ruangan=ruangan,
        ).exists()
        if existing:
            validation_error_messages['schedule_exist'] = 'Schedule is already exist!'

        # check apakah untuk di Waktu ke-X, kelas Y menerima lebih dari 1 mata pelajaran?
        existing_2 = Jadwal.objects.filter(
            detail_waktu=detail_waktu,
            detail_pelajaran__kelas_peserta__id=detail_pelajaran.kelas_peserta.id
        )
        if existing_2.exists():
            jadwal = existing_2[0]
            # kalau detail pelajaran dari database dengan yang diinputkan user sama, maka itu hanya update, selain itu maka munculkan error sesuai constraint
            if jadwal.detail_pelajaran != detail_pelajaran:
                error_messages = "{} has got a lesson schedule {} in during class hours {}".format(
                    jadwal.detail_pelajaran.kelas_peserta,
                    jadwal.detail_pelajaran.mapel.mapel,
                    jadwal.detail_waktu
                )
                validation_error_messages['course_in_class_exist'] = error_messages

        # check apakah untuk di Waktu ke-X, ruangan Y menerima lebih dari 1 mata pelajaran?
        existing_3 = Jadwal.objects.filter(
            detail_waktu=detail_waktu,
            ruangan=ruangan
        )
        if existing_3.exists():
            jadwal = existing_3[0]
            # kalau detail pelajaran dari database dengan yang diinputkan user sama, maka itu hanya update, selain itu maka munculkan error sesuai constraint
            if jadwal.detail_pelajaran != detail_pelajaran:
                error_messages = "{} at time {} has been plotted for lesson schedule {}".format(
                    jadwal.ruangan.nama_ruangan,
                    jadwal.detail_waktu,
                    jadwal.detail_pelajaran.mapel.mapel
                )
                validation_error_messages['room_has_taken_at_this_time'] = error_messages

        # check apakah untuk di waktu ke-X, Guru Y mengajar lebih dari 1 mata pelajaran?
        existing_4 = Jadwal.objects.filter(
            detail_waktu=detail_waktu,
            guru=guru
        )
        if existing_4.exists():
            jadwal = existing_4[0]
            # kalau detail pelajaran dari database dengan yang diinputkan user sama, maka itu hanya update, selain itu maka munculkan error sesuai constraint
            if jadwal.detail_pelajaran != detail_pelajaran:
                error_messages = "Teacher {} is plotted to teach {} at time {}. So, one teacher cannot teach two subjects at the same time".format(
                    jadwal.guru.nama_lengkap,
                    jadwal.detail_pelajaran.mapel.mapel,
                    jadwal.detail_waktu,
                )
                validation_error_messages['teachers_in_one_time_exist'] = error_messages

        # check apakah jam pelajaran suatu mapel sudah melebihi batas?
        existing_5 = Jadwal.objects.filter(
            detail_pelajaran=detail_pelajaran
        )
        if existing_5.exists():
            jadwal = existing_5[0]
            total_jam = jadwal.detail_pelajaran.total_jam
            daftar_kode_waktu = list()
            if total_jam == existing_5.count():
                # masukan daftar detail_waktu unique yang diperoleh dari hasil query
                for mapel in existing_5:
                    if mapel.detail_waktu not in daftar_kode_waktu:
                        daftar_kode_waktu.append(mapel.detail_waktu)
                # check apakah detail_waktu yang diinput user ada di daftar_kode_waktu? kalau iya maka hanya update data, selain itu munculkan warning
                if detail_waktu not in daftar_kode_waktu:
                    error_messages = "Class {} should receive {} hours of {} lessons".format(
                        jadwal.detail_pelajaran.kelas_peserta,
                        jadwal.detail_pelajaran.total_jam,
                        jadwal.detail_pelajaran.mapel.mapel,
                    )
                    validation_error_messages['maximum_time_schedule_exceed'] = error_messages

        # munculkan semua validation error yang ada terakhir
        if len(validation_error_messages) > 0:
            list_validation_error_messages = list()
            for key_error, message in validation_error_messages.items():
                list_validation_error_messages.append(
                    ValidationError(
                        message, code=key_error)
                )
            list_validation_error_messages.append(
                ValidationError(
                    'Please check your input!', code='check_input')
            )
            raise forms.ValidationError(list_validation_error_messages)

        return cleaned_data

    # def clean_detail_pelajaran(self):
    #     form_detail_pelajaran = self.cleaned_data.get('detail_pelajaran')
    #     existing = Jadwal.objects.filter(
    #         detail_pelajaran=form_detail_pelajaran)
    #     if existing:
    #         raise forms.ValidationError('Pelajaran Sudah Ada')
    #     return form_detail_pelajaran
