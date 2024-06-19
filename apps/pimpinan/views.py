from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from administrator.models import (
    Hari,
)
from tenagapengajar.models import (
    Jadwal
)
from .forms import (
    RevisiJadwalForm,
)
from .models import RevisiJadwal


class RevisiJadwalListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = RevisiJadwal
    template_name = "pimpinan/revisi_jadwal_list.html"
    context_object_name = 'revisi_jadwal_list'
    extra_context = {
        'title_page': 'Schedule | Revisi',
        'subtitle_page': "Daftar Jadwal Direvisi",
    }

    def get_queryset(self):
        revisi_jadwal_list = dict()
        days = Hari.objects.values_list('nama_hari', flat=True).distinct()

        # Buat dictionary untuk setiap kelas di setiap hari
        for hari in days:
            # filter juga sesuai nama guru yang login ke sistem, revisi jadwal spesifik ke setiap guru yang bersangkutan
            revisi_jadwal_list[hari] = self.model.objects.filter(
                jadwal__detail_waktu__hari__nama_hari__iexact=str(hari)
            ).order_by('jadwal__detail_waktu')
        self.queryset = {
            'revisi_jadwal_list': revisi_jadwal_list,
            'days': days,
        }
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        # merge dictionary context yang sebelumnya dengan extra context
        self.kwargs.update(self.extra_context)
        kwargs = self.kwargs
        return super().get_context_data(**kwargs)

    def test_func(self):
        return self.request.user.groups.filter(name='pimpinan')


class RevisiJadwalCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = RevisiJadwal
    form_class = RevisiJadwalForm
    template_name = 'create.html'
    extra_context = {
        'title_page': 'Manage Revisi Jadwal | Tambah',
        'subtitle_page': "Tambah Data Revisi Jadwal",
        'button': {
            'button_color': 'btn-success',
            'button_name': 'Tambah'
        },
        'back_url': 'pimpinan:revisi_jadwal_list'
    }
    success_url = reverse_lazy("pimpinan:revisi_jadwal_list")
    success_message = ''

    # method untuk memperbarui select option sesuai primary key jadwal pada url
    def get_initial(self):
        id_jadwal = self.kwargs['pk']
        # ambil jadwal based on id_jadwal
        jadwal = Jadwal.objects.filter(pk=id_jadwal)
        # get the initial dictionary from the superclass method
        initial = super(RevisiJadwalCreateView, self).get_initial()
        # copy the dictionary
        initial = initial.copy()
        if len(jadwal) == 1:
            initial['jadwal'] = jadwal[0]
        return initial

    def form_valid(self, form):
        form.save()
        self.success_message = '%(mapel)s | %(kelas_peserta)s  was updated successfully' % {
            'mapel': form.cleaned_data.get('jadwal').detail_pelajaran.mapel.mapel,
            'kelas_peserta': form.cleaned_data.get('jadwal').detail_pelajaran.kelas_peserta,
        }
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        # merge dictionary context yang sebelumnya dengan extra context
        self.kwargs.update(self.extra_context)
        kwargs = self.kwargs
        return super().get_context_data(**kwargs)

    def test_func(self):
        return self.request.user.groups.filter(name='pimpinan')


class RevisiJadwalUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = RevisiJadwal
    form_class = RevisiJadwalForm
    template_name = 'create.html'
    extra_context = {
        'title_page': 'Manage Jadwal | Update',
        'subtitle_page': "Update Jadwal",
        'button': {
            'button_color': 'btn-warning',
            'button_name': 'Update'
        },
        'back_url': 'pimpinan:revisi_jadwal_list'
    }
    success_url = reverse_lazy("pimpinan:revisi_jadwal_list")
    success_message = ''

    def form_valid(self, form):
        form.save()
        self.success_message = '%(mapel)s | %(kelas_peserta)s  was updated successfully' % {
            'mapel': form.cleaned_data.get('jadwal').detail_pelajaran.mapel.mapel,
            'kelas_peserta': form.cleaned_data.get('jadwal').detail_pelajaran.kelas_peserta,
        }
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        self.kwargs.update(self.extra_context)
        kwargs = self.kwargs
        return super().get_context_data(**kwargs)

    def test_func(self):
        return self.request.user.groups.filter(name='pimpinan')


class RevisiJadwalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RevisiJadwal
    template_name = 'delete_confirmation.html'
    success_url = reverse_lazy('pimpinan:revisi_jadwal_list')
    context_object_name = 'object_deleted'
    success_message = 'Data was deleted successfully'
    extra_context = {
        'title_page': 'Manage Revisi Jadwal | Delete',
        'subtitle_page': "Revisi Jadwal delete confirmation",
        'entity': 'Revisi Jadwal',
        'back_url': 'pimpinan:revisi_jadwal_list'
    }

    def get_context_data(self, **kwargs):
        # mengganti tulisan pada object_deleted
        object_text = str(
            self.object.jadwal.detail_pelajaran.mapel) + " | " + str(self.object.jadwal.guru.nama_lengkap) + " | " + str(self.object.jadwal.detail_waktu.hari) + " | " + str(self.object.jadwal.detail_waktu.waktu)

        # merge dictionary context yang sebelumnya dengan extra context
        self.extra_context['sub_object_deleted'] = "Pesan Revisi: " + \
            str(self.object.revisi_messages)
        self.kwargs.update(self.extra_context)
        kwargs = self.kwargs

        # replace self.object dengan object text terbaru
        self.object = object_text

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name='pimpinan')


def error_404_view(request, exception):
    return render(request, '404.html')


def pimpinan_group(user):
    return user.groups.filter(name='pimpinan')


@login_required
@user_passes_test(pimpinan_group)
def validasi_all_jadwal(request, **kwargs):
    template_name = 'jadwal/list.html'
    context = {
        'title_page': 'Manage Jadwal | Lock All',
    }
    if kwargs['status_validasi'] == 'Lock':
        Jadwal.objects.update(status_validasi='Lock')
    elif kwargs['status_validasi'] == "Unlock":
        Jadwal.objects.update(status_validasi='Unlock')
    return redirect('jadwal_list')


@login_required
@user_passes_test(pimpinan_group)
def lock_jadwal(request, **kwargs):
    template_name = 'jadwal/list.html'
    context = {
        'title_page': 'Manage Jadwal | Lock',
    }
    print(kwargs)
    if kwargs['pk']:
        # ambil primary key dari jadwal yang ingin di lock
        id_jadwal = kwargs['pk']

        # update jadwal tersebut
        Jadwal.objects.filter(pk=id_jadwal).update(status_validasi='Lock')

        return redirect('jadwal_list')
    else:
        return redirect('index')


@login_required
@user_passes_test(pimpinan_group)
def unlock_specific_jadwal(request, **kwargs):
    template_name = 'jadwal/list.html'
    context = {
        'title_page': 'Manage Jadwal | Unlock',
    }
    if kwargs['pk']:
        # ambil primary key dari jadwal yang ingin di lock
        id_jadwal = kwargs['pk']

        # update jadwal tersebut
        Jadwal.objects.filter(pk=id_jadwal).update(status_validasi='Unlock')

        return redirect('jadwal_list')
    else:
        return redirect('index')
