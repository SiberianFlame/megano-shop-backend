from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from megano_auth.forms import UserRegistrationForm


class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'frontend/signUp.html'
    success_url = reverse_lazy('frontend:index-page')

    def form_valid(self, form):
        print('register view is working')
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(
            self.request,
            username=username,
            password=password)

        login(request=self.request, user=user)
        return response
