from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView
)
from administrator.models import Hari
from pimpinan.models import RevisiJadwal
from .forms import (
    JadwalForm,
)
from .models import (
    Jadwal,
)
# Create your views here.


class JadwalCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    form_class = JadwalForm
    template_name = 'jadwal/create.html'
    extra_context = {
        'title_page': 'Manage Jadwal | Tambah',
        'subtitle_page': "Tambah Data Jadwal",
        'button': {
            'button_color': 'btn-success',
            'button_name': 'Tambah'
        },
        'back_url': 'jadwal_list'
    }
    success_url = reverse_lazy("tenagapengajar:jadwal_create")
    success_message = '%(detail_pelajaran)s | %(guru)s | %(detail_waktu)s was created successfully'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        # merge dictionary context yang sebelumnya dengan extra context
        self.kwargs.update(self.extra_context)
        kwargs = self.kwargs
        return super().get_context_data(**kwargs)

    # overide method UserPassedTestMixin hanya tenagapengajar yang bisa create jadwal
    def test_func(self):
        return self.request.user.groups.filter(name='tenagapengajar')


class JadwalUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Jadwal
    form_class = JadwalForm
    template_name = 'jadwal/create.html'
    extra_context = {
        'title_page': 'Manage Jadwal | Update',
        'subtitle_page': "Update Jadwal",
        'button': {
            'button_color': 'btn-warning',
            'button_name': 'Update'
        },
        'back_url': 'jadwal_list'
    }
    success_url = reverse_lazy("jadwal_list")
    success_message = '%(detail_pelajaran)s | %(guru)s | %(detail_waktu)s was updated successfully'

    def form_valid(self, form):
        instance = form.save()
        is_this_jadwal_has_revisi, revised_jadwal = form.check_if_revisi_jadwal_exist_with_this_updated_jadwal(
            id=instance.id)
        if is_this_jadwal_has_revisi > 0:
            # delete revisi jadwal yang bersangkutan baru dari tabel RevisiJadwal
            deleted_row_revisi_jadwal = revised_jadwal.delete()

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        self.kwargs.update(self.extra_context)
        kwargs = self.kwargs
        return super().get_context_data(**kwargs)

    def test_func(self):
        return self.request.user.groups.filter(name='tenagapengajar')


class JadwalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Jadwal
    template_name = 'delete_confirmation.html'
    success_url = reverse_lazy('jadwal_list')
    context_object_name = 'object_deleted'
    success_message = 'Data was deleted successfully'
    extra_context = {
        'title_page': 'Manage Jadwal | Delete',
        'subtitle_page': "Jadwal delete confirmation",
        'entity': 'Jadwal',
        'back_url': 'jadwal_list'
    }

    def get_context_data(self, **kwargs):
        # merge dictionary context yang sebelumnya dengan extra context
        self.kwargs.update(self.extra_context)
        kwargs = self.kwargs
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name='tenagapengajar')


class RevisiJadwalListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = RevisiJadwal
    template_name = "tenagapengajar/revisi_jadwal_list.html"
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
        return self.request.user.groups.filter(name='tenagapengajar')
