from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import RuanganForms
from .models import Ruangan
from django.http import JsonResponse


class RuanganListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Ruangan
    template_name = "administrator/ruangan/list.html"
    context_object_name = 'ruangan_list'

    extra_context = {
        'title_page': 'Database | Ruangan',
        'subtitle_page': "Daftar Ruangan",
    }

    def get_context_data(self, **kwargs):
        # merge dictionary context yang sebelumnya dengan extra context
        self.kwargs.update(self.extra_context)
        kwargs = self.kwargs
        return super().get_context_data(**kwargs)

    def test_func(self):
        return self.request.user.groups.filter(name='administrator')


class RuanganCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    form_class = RuanganForms
    template_name = 'create.html'
    extra_context = {
        'title_page': 'Manage Ruangan | Tambah',
        'subtitle_page': "Tambah Data Ruangan",
        'button': {
            'button_color': 'btn-success',
            'button_name': 'Tambah'
        },
        'back_url': 'administrator_IT:ruangan_list'
    }
    success_url = reverse_lazy("administrator_IT:ruangan_create")
    success_message = '%(kode_ruangan)s | %(nama_ruangan)s was created successfully'

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

    def test_func(self):
        return self.request.user.groups.filter(name='administrator')


class RuanganUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Ruangan
    form_class = RuanganForms
    template_name = 'create.html'
    extra_context = {
        'title_page': 'Manage Ruangan | Update',
        'subtitle_page': "Update Ruangan",
        'button': {
            'button_color': 'btn-warning',
            'button_name': 'Update'
        },
        'back_url': 'administrator_IT:ruangan_list'
    }
    success_url = reverse_lazy("administrator_IT:ruangan_list")
    success_message = '%(kode_ruangan)s | %(nama_ruangan)s was updated successfully'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        self.kwargs.update(self.extra_context)
        kwargs = self.kwargs
        return super().get_context_data(**kwargs)

    def test_func(self):
        return self.request.user.groups.filter(name='administrator')


class RuanganDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ruangan
    template_name = 'delete_confirmation.html'
    success_url = reverse_lazy('administrator_IT:ruangan_list')
    context_object_name = 'object_deleted'
    success_message = 'Data was deleted successfully'

    extra_context = {
        'title_page': 'Manage Ruangan | Update',
        'subtitle_page': "Ruangan delete confirmation",
        'entity': 'Ruangan',
        'back_url': 'administrator_IT:ruangan_list'
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
        return self.request.user.groups.filter(name='administrator')


def search_ruangan(request):
    keyword = request.GET.get('keyword', None)
    # buat query untuk menjadi mata pelajaran dan kelas berdasarkan keyword
    response_query = Ruangan.objects.filter(
        nama_ruangan__icontains=keyword,
    ).values()

    # ambil hasil jquery response
    data = {
        'ruangan': list(response_query)
    }

    return JsonResponse(data)
