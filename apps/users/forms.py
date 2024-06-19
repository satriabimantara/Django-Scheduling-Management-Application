from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UpdateUserForm(forms.ModelForm):
    username_old = forms.CharField(widget=forms.HiddenInput())
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username_old', 'username',
                  'email', 'first_name', 'last_name']

    def clean(self, *args, **kwargs):
        username_old = self.cleaned_data.get('username_old')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        # # cek kalau email dari user yang login sudah ada di database
        # check_old_user_email = User.objects.filter(email=email)
        # if check_old_user_email.count():
        #     username_database =check_old_user_email[0].username
        #     # cek apakah user hanya mengganti username
        #     if username_old == username_database:
        #         raise forms.ValidationError(
        #             'This email address is already in use. Please supply a different email address.')

        # # cek apakah yang diubah hanya usernamenya saja
        # if username == username_old:
        #     # baru cek apakah email sudah ada di database atau tidak
        #     if User.objects.filter(email=email).exclude(username=username).count():
        #         raise forms.ValidationError(
        #         'This email address is already in use. Please supply a different email address.')
        # else:
        #     # yang diubah ternyata username dari user yang login

        # cek apakah email sudah exist
        if email and User.objects.filter(email=email).count():
            if User.objects.filter(email=email).exclude(username=username_old).count():
                raise forms.ValidationError(
                    'This email address is already in use. Please supply a different email address.')
        # cek apakah username sudah ada?
        if User.objects.filter(username=username).count():
            # kalau username old ga sama dengan yang diretrieve dari database raise error
            if username_old != User.objects.filter(username=username)[0].username:
                raise forms.ValidationError(
                    'This username is already in use. Please supply a different username.')
        return self.cleaned_data

    # def save(self, commit=True):
    #     user = super(RegistrationForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']

    #     if commit:
    #         user.save()

    #     return user


class UpdateProfileForm(forms.ModelForm):
    # avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['bio']
