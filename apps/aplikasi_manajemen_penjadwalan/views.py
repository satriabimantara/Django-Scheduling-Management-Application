from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import UserForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView
from django.views.generic import (
    ListView,
)
from tenagapengajar.models import (
    Jadwal,
)
from administrator.models import (
    Hari
)


class IndexView(LoginRequiredMixin, View):
    template_name = 'index.html'
    context = {
        'title_page': "Home",
        'subtitle_page': 'Halaman Home'
    }

    def get(self, request, **params):
        return render(request, self.template_name, self.context)


class JadwalListView(LoginRequiredMixin, ListView):
    model = Jadwal
    template_name = "jadwal/list.html"
    context_object_name = 'jadwal_list'
    extra_context = {
        'title_page': 'Schedule | Lihat',
        'subtitle_page': "Daftar Jadwal Pelajaran",
    }

    def get_queryset(self):
        jadwal_list = dict()
        days = Hari.objects.values_list('nama_hari', flat=True).distinct()

        # Buat dictionary untuk setiap kelas di setiap hari
        for hari in days:
            jadwal_list[hari] = self.model.objects.filter(
                detail_waktu__hari__nama_hari__iexact=str(hari),
            ).order_by('detail_waktu')
        self.queryset = {
            'jadwal_list': jadwal_list,
            'days': days,
        }
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        # merge dictionary context yang sebelumnya dengan extra context
        self.kwargs.update(self.extra_context)
        kwargs = self.kwargs
        return super().get_context_data(**kwargs)


def error_404_view(request, exception):
    return render(request, '404.html')


class UserLoginView(LoginView):
    template_name = 'login.html'
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(RegisterView, self).get(*args, **kwargs)
