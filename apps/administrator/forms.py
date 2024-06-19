from django import forms
from .models import (
    DetailMataPelajaran,
    Guru,
    MataPelajaran,
    Ruangan,
    DetailKelas,
    Waktu,
    DetailWaktu,
)


class GuruForms(forms.ModelForm):
    class Meta:
        model = Guru
        fields = [
            'nip',
            'nama_lengkap'
        ]
        labels = {
            'nama_lengkap': "Nama Lengkap Guru (dengan gelar)"
        }
        widgets = {
            'nip': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'autofocus': 'True'
                }
            ),
            'nama_lengkap': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class MataPelajaranForms(forms.ModelForm):
    class Meta:
        model = MataPelajaran
        fields = [
            'kode_mapel',
            'mapel'
        ]
        widgets = {
            'kode_mapel': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'autofocus': 'True'
                }
            ),
            'mapel': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class RuanganForms(forms.ModelForm):
    class Meta:
        model = Ruangan
        fields = [
            'kode_ruangan',
            'nama_ruangan',
            'kapasitas_ruangan',
        ]
        labels = {
            'kode_ruangan': "Kode Unik Ruangan"
        }
        widgets = {
            'kode_ruangan': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'autofocus': 'True'
                }
            ),
            'nama_ruangan': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'kapasitas_ruangan': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class DetailKelasForms(forms.ModelForm):
    class Meta:
        model = DetailKelas
        fields = [
            'kelas',
            'jalur',
        ]
        widgets = {
            'kelas': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'jalur': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        kelas = cleaned_data.get('kelas')
        jalur = cleaned_data.get('jalur')

        # check apakah sudah ada kelas dan jalur yang sama di DB
        existing_same_kelas_and_jalur = DetailKelas.objects.filter(
            kelas=kelas,
            jalur=jalur
        ).exists()
        if existing_same_kelas_and_jalur:
            raise forms.ValidationError(
                'Kelas with the same Jalur is already exist!', code='kelas_jalur_exist')
        return cleaned_data


class DetailMataPelajaranForm(forms.ModelForm):
    class Meta:
        model = DetailMataPelajaran
        fields = [
            'mapel',
            'kelas_peserta',
            'total_jam'
        ]
        widgets = {
            'mapel': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'kelas_peserta': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'total_jam': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'required': 'true'
                }
            ),
        }

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        mapel = cleaned_data.get('mapel')
        kelas_peserta = cleaned_data.get('kelas_peserta')
        total_jam_old = cleaned_data.get('total_jam_old')
        print(cleaned_data)

        # check apakah sudah ada mapel dan kelas peserta yang sama di DB
        existing_same_mapel_and_kelas_peserta = DetailMataPelajaran.objects.filter(
            mapel=mapel,
            kelas_peserta=kelas_peserta,
        )

        if existing_same_mapel_and_kelas_peserta.exists():
            # if total_jam_old == existing_same_mapel_and_kelas_peserta[0].total_jam:

            raise forms.ValidationError(
                'Mata Pelajaran with the same Kelas Peserta is already exist!', code='mapel_kelas_exist')

        return cleaned_data


class WaktuForm(forms.ModelForm):
    class Meta:
        model = Waktu
        fields = [
            'nama_waktu',
        ]
        widgets = {
            'nama_waktu': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '08.00 - 08.40 WITA',
                    'autofocus': 'True'
                },
            ),
        }


class DetailWaktuForm(forms.ModelForm):
    class Meta:
        model = DetailWaktu
        fields = [
            'hari',
            'waktu'
        ]
        widgets = {
            'hari': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'waktu': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        hari = cleaned_data.get('hari')
        waktu = cleaned_data.get('waktu')

        # check apakah sudah ada hari dan waktu yang sama di DB
        existing_same_hari_dan_waktu = DetailWaktu.objects.filter(
            hari=hari,
            waktu=waktu
        ).exists()
        if existing_same_hari_dan_waktu:
            raise forms.ValidationError(
                'Hari with the same Waktu is already exist!', code='hari_waktu_exist')
        return cleaned_data
