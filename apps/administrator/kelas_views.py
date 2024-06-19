from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import DetailKelasForms
from .models import (
    DetailKelas,
    Kelas,
    Jalur
)


class KelasIndexView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'administrator/kelas/index.html'
    context = {
        'title_page': "Database | Kelas",
        'subtitle_page': "Halaman Database Kelas"
    }

    def get(self, request):
        all_class = Kelas.objects.all()
        all_jalur = Jalur.objects.all()
        all_detailkelas = DetailKelas.objects.all()
        self.context.update(
            {
                'all_class': all_class,
                'all_jalur': all_jalur,
                'all_detailkelas': all_detailkelas,
            }
        )
        return render(request, self.template_name, self.context)

    def test_func(self):
        return self.request.user.groups.filter(name='administrator')


class DetailKelasCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    form_class = DetailKelasForms
    template_name = 'create.html'
    extra_context = {
        'title_page': 'Manage Kelas Peserta | Tambah',
        'subtitle_page': "Tambah Data Kelas Peserta",
        'button': {
            'button_color': 'btn-success',
            'button_name': 'Tambah'
        },
        'back_url': 'administrator_IT:kelas_list'
    }
    success_url = reverse_lazy("administrator_IT:kelas_create")
    success_message = '%(kelas)s | %(jalur)s was created successfully'

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


class DetailKelasUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = DetailKelas
    form_class = DetailKelasForms
    template_name = 'create.html'
    extra_context = {
        'title_page': 'Manage Kelas Peserta | Update',
        'subtitle_page': "Update Data Kelas Peserta",
        'button': {
            'button_color': 'btn-warning',
            'button_name': 'Update'
        },
        'back_url': 'administrator_IT:kelas_list'
    }
    success_url = reverse_lazy("administrator_IT:kelas_list")
    success_message = '%(kelas)s | %(jalur)s was updated successfully'

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


class DetailKelasDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DetailKelas
    template_name = 'delete_confirmation.html'
    success_url = reverse_lazy('administrator_IT:kelas_list')
    context_object_name = 'object_deleted'
    success_message = 'Data was deleted successfully'

    extra_context = {
        'title_page': 'Manage Detail Kelas | Delete',
        'subtitle_page': "Detail Kelas delete confirmation",
        'entity': 'Detail Kelas',
        'back_url': 'administrator_IT:kelas_list'
    }

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # merge dictionary context yang sebelumnya dengan extra context
        self.kwargs.update(self.extra_context)
        kwargs = self.kwargs
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name='administrator')


def search_kelas_peserta(request):
    keyword = request.GET.get('keyword', None)
    keyword = keyword.split(' ')
    # contoh hasil split ['matematika', 'X']
    if len(keyword) == 1:
        # buat query untuk menjadi mata pelajaran dan kelas berdasarkan keyword
        response_query = DetailKelas.objects.filter(
            kelas__nama_kelas__icontains=keyword[0],
        ).values()
    elif len(keyword) == 2:
        response_query = DetailKelas.objects.filter(
            kelas__nama_kelas__icontains=keyword[0],
            jalur__nama_jalur__icontains=keyword[1],
        ).values()
    # ambil hasil jquery response
    data = {
        'kelas_peserta': list(response_query)
    }

    return JsonResponse(data)
