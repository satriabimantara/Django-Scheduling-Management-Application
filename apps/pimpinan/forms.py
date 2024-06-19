from django import forms
from .models import (
    RevisiJadwal
)


class RevisiJadwalForm(forms.ModelForm):
    class Meta:
        model = RevisiJadwal
        fields = "__all__"
        widgets = {
            'jadwal': forms.Select(
                attrs={
                    'class': 'form-control',
                    'required': 'True'
                }
            ),
            'revisi_messages': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'required': 'True',
                    "max_length": 10
                }
            ),
        }
