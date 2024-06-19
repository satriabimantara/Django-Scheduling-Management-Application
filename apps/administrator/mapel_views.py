from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from django.core.serializers import serialize
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import MataPelajaranForms, DetailMataPelajaranForm
from .models import MataPelajaran, DetailMataPelajaran


class MataPelajaranIndexView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'administrator/mapel/index.html'
    context = {
        'title_page': "Database | Mata Pelajaran",
        'subtitle_page': "Halaman Database Mata Pelajaran"
    }

    def get(self, request):
        all_mapel = MataPelajaran.objects.all()
        self.context.update(
            {
                'all_mapel': all_mapel,
            }
        )
        return render(request, self.template_name, self.context)

    def test_func(self):
        return self.request.user.groups.filter(name='administrator')


class DetailMataPelajaranIndexView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'administrator/mapel/index_detail_mapel.html'
    context = {
        'title_page': "Database | Mapping Mata Pelajaran",
        'subtitle_page': "Halaman Mapping Mata Pelajaran"
    }

    def get(self, request):
        all_detailmapel = DetailMataPelajaran.objects.all()
        self.context.update(
            {
                'all_detailmapel': all_detailmapel,
            }
        )
        return render(request, self.template_name, self.context)

    def test_func(self):
        return self.request.user.groups.filter(name='administrator')


class DetailMataPelajaranCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    form_class = DetailMataPelajaranForm
    template_name = 'administrator/mapel/create_detail_mata_pelajaran.html'
    extra_context = {
        'title_page': 'Manage Detail Mapel | Tambah',
        'subtitle_page': "Tambah Detail Mata Pelajaran",
        'button': {
            'button_color': 'btn-success',
            'button_name': 'Tambah'
        },
        'back_url': 'administrator_IT:detail_mata_pelajaran_list'
    }
    success_url = reverse_lazy("administrator_IT:detail_mata_pelajaran_create")
    success_message = '%(mapel)s  | %(kelas_peserta)s was created successfully'

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


class DetailMataPelajaranUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = DetailMataPelajaran
    form_class = DetailMataPelajaranForm
    template_name = 'create.html'
    extra_context = {
        'title_page': 'Manage Detail Mapel | Update',
        'subtitle_page': "Update Detail Mata Pelajaran",
        'button': {
            'button_color': 'btn-warning',
            'button_name': 'Update'
        },
        'back_url': 'administrator_IT:detail_mata_pelajaran_list'
    }
    success_url = reverse_lazy("administrator_IT:detail_mata_pelajaran_list")
    success_message = '%(kode_detailmapel)s | %(mapel)s  | %(kelas_peserta)s was updated successfully'

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


class DetailMataPelajaranDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DetailMataPelajaran
    template_name = 'delete_confirmation.html'
    success_url = reverse_lazy('administrator_IT:detail_mata_pelajaran_list')
    context_object_name = 'object_deleted'
    success_message = 'Data was deleted successfully'

    extra_context = {
        'title_page': 'Manage Detail Mapel | Delete',
        'subtitle_page': "Detail Mata Pelajaran delete confirmation",
        'entity': 'Detail Mata Pelajaran',
        'back_url': 'administrator_IT:detail_mata_pelajaran_list'
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


class MataPelajaranCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    form_class = MataPelajaranForms
    template_name = 'create.html'
    extra_context = {
        'title_page': 'Manage Mapel | Tambah',
        'subtitle_page': "Tambah Data Mata Pelajaran",
        'button': {
            'button_color': 'btn-success',
            'button_name': 'Tambah'
        },
        'back_url': 'administrator_IT:mata_pelajaran_list'
    }
    success_url = reverse_lazy("administrator_IT:mata_pelajaran_create")
    success_message = '%(kode_mapel)s | %(mapel)s was created successfully'

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


class MataPelajaranUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = MataPelajaran
    form_class = MataPelajaranForms
    template_name = 'create.html'
    extra_context = {
        'title_page': 'Manage Mapel | Update',
        'subtitle_page': "Update Data Mata Pelajaran",
        'button': {
            'button_color': 'btn-warning',
            'button_name': 'Update'
        },
        'back_url': 'administrator_IT:mata_pelajaran_list'
    }
    success_url = reverse_lazy("administrator_IT:mata_pelajaran_list")
    success_message = '%(kode_mapel)s | %(mapel)s was updated successfully'

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


class MataPelajaranDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MataPelajaran
    template_name = 'delete_confirmation.html'
    success_url = reverse_lazy('administrator_IT:mata_pelajaran_list')
    context_object_name = 'object_deleted'
    success_message = 'Data was deleted successfully'

    extra_context = {
        'title_page': 'Manage Mapel | Delete',
        'subtitle_page': "Mata Pelajaran delete confirmation",
        'entity': 'Mata Pelajaran',
        'back_url': 'administrator_IT:mata_pelajaran_list'
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


# AJAX FUNCTION FOR SEARCHING KEYWORDS
def search_detail_pelajaran(request):
    keyword = request.GET.get('keyword', None)
    keyword = keyword.split(' ')
    # contoh hasil split ['matematika', 'X']
    if len(keyword) == 1:
        # buat query untuk menjadi mata pelajaran dan kelas berdasarkan keyword
        response_query = DetailMataPelajaran.objects.filter(
            mapel__mapel__icontains=keyword[0],
        ).values()
    elif len(keyword) == 2:
        response_query = DetailMataPelajaran.objects.filter(
            mapel__mapel__icontains=keyword[0],
            kelas_peserta__kelas__nama_kelas__icontains=keyword[1]
        ).values()
    # ambil hasil jquery response
    data = {
        'detail_pelajaran': list(response_query)
    }

    return JsonResponse(data)


def search_mapel(request):
    keyword = request.GET.get('keyword', None)
    # buat query untuk menjadi mata pelajaran dan kelas berdasarkan keyword
    response_query = MataPelajaran.objects.filter(
        mapel__icontains=keyword,
    ).values()

    # ambil hasil jquery response
    data = {
        'mapel': list(response_query)
    }

    return JsonResponse(data)
