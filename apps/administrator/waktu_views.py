from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import WaktuForm, DetailWaktuForm
from .models import Waktu, DetailWaktu
from django.http import JsonResponse


class WaktuIndexView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'administrator/waktu/index.html'
    context = {
        'title_page': "Database | Waktu",
        'subtitle_page': "Halaman Database Waktu Pelajaran"
    }

    def get(self, request):
        all_waktu = Waktu.objects.all()
        all_detailwaktu = DetailWaktu.objects.all()
        self.context.update(
            {
                'all_waktu': all_waktu,
                'all_detailwaktu': all_detailwaktu,
            }
        )
        return render(request, self.template_name, self.context)

    def test_func(self):
        return self.request.user.groups.filter(name='administrator')


class DetailWaktuCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    form_class = DetailWaktuForm
    template_name = 'create.html'
    extra_context = {
        'title_page': 'Manage Detail Waktu | Tambah',
        'subtitle_page': "Tambah Detail Waktu",
        'button': {
            'button_color': 'btn-success',
            'button_name': 'Tambah'
        },
        'back_url': 'administrator_IT:waktu_list'
    }
    success_url = reverse_lazy("administrator_IT:detail_waktu_create")
    success_message = '%(hari)s  | %(waktu)s was created successfully'

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


class DetailWaktuUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = DetailWaktu
    form_class = DetailWaktuForm
    template_name = 'create.html'
    extra_context = {
        'title_page': 'Manage Detail Waktu | Update',
        'subtitle_page': "Update Detail Waktu",
        'button': {
            'button_color': 'btn-warning',
            'button_name': 'Update'
        },
        'back_url': 'administrator_IT:waktu_list'
    }
    success_url = reverse_lazy("administrator_IT:waktu_list")
    success_message = '%(hari)s  | %(waktu)s was updated successfully'

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


class DetailWaktuDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DetailWaktu
    template_name = 'delete_confirmation.html'
    success_url = reverse_lazy('administrator_IT:waktu_list')
    context_object_name = 'object_deleted'
    success_message = 'Data was deleted successfully'

    extra_context = {
        'title_page': 'Manage Detail Waktu | Delete',
        'subtitle_page': "Detail Waktu delete confirmation",
        'entity': 'Detail Waktu',
        'back_url': 'administrator_IT:waktu_list'
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


class WaktuCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    form_class = WaktuForm
    template_name = 'create.html'
    extra_context = {
        'title_page': 'Manage Waktu | Tambah',
        'subtitle_page': "Tambah Data Waktu",
        'button': {
            'button_color': 'btn-success',
            'button_name': 'Tambah'
        },
        'back_url': 'administrator_IT:waktu_list'
    }
    success_url = reverse_lazy("administrator_IT:waktu_create")
    success_message = '%(nama_waktu)s was created successfully'

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


class WaktuUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Waktu
    form_class = WaktuForm
    template_name = 'create.html'
    extra_context = {
        'title_page': 'Manage Waktu | Update',
        'subtitle_page': "Update Data Waktu",
        'button': {
            'button_color': 'btn-warning',
            'button_name': 'Update'
        },
        'back_url': 'administrator_IT:waktu_list'
    }
    success_url = reverse_lazy("administrator_IT:waktu_list")
    success_message = '%(nama_waktu)s was updated successfully'

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


class WaktuDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Waktu
    template_name = 'delete_confirmation.html'
    success_url = reverse_lazy('administrator_IT:waktu_list')
    context_object_name = 'object_deleted'
    success_message = 'Data was deleted successfully'

    extra_context = {
        'title_page': 'Manage Waktu | Delete',
        'subtitle_page': "Waktu delete confirmation",
        'entity': 'Waktu',
        'back_url': 'administrator_IT:waktu_list'
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


def search_detail_waktu(request):
    keyword = request.GET.get('keyword', None)
    keyword = keyword.split(' ')
    # contoh hasil split ['senin', '08.00']
    if len(keyword) == 1:
        # buat query untuk menjadi mata pelajaran dan kelas berdasarkan keyword
        response_query = DetailWaktu.objects.filter(
            hari__nama_hari__icontains=keyword[0],
        ).values()
    elif len(keyword) == 2:
        response_query = DetailWaktu.objects.filter(
            hari__nama_hari__icontains=keyword[0],
            waktu__nama_waktu__icontains=keyword[1]
        ).values()

    # ambil hasil jquery response
    data = {
        'detail_waktu': list(response_query)
    }

    return JsonResponse(data)
