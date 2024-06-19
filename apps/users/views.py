from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import UpdateUserForm, UpdateProfileForm
from .forms import UpdateProfileForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
# Create your views here.


def is_member(user):
    return user.groups.filter(name='administrator').exists() or user.groups.filter(name='pimpinan').exists() or user.groups.filter(name='tenagapengajar').exists()


@login_required
@user_passes_test(is_member)
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users:profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
        # menambahkan initial value pada input hidden pada user_form
        user_form.fields['username_old'].initial = request.user.username

    return render(request, 'users/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


class ChangePasswordView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('logout')

    def test_func(self):
        return self.request.user.groups.filter(name='pimpinan') or self.request.user.groups.filter(name='administrator') or self.request.user.groups.filter(name='tenagapengajar')


class UserProfileIndexView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'users/index.html'
    context = {
        'title_page': "User Profile",
    }

    def get(self, request):
        return render(request, self.template_name, self.context)

    def test_func(self):
        return self.request.user.groups.filter(name='pimpinan') or self.request.user.groups.filter(name='administrator') or self.request.user.groups.filter(name='tenagapengajar')
