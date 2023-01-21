from django.shortcuts import render, redirect
from .forms import CreateUser
from django.views.generic import CreateView


class NewUser(CreateView):
    template_name = 'registration/register.html'
    form_class = CreateUser

    def form_valid(self, form):
        form.save()
        return redirect('login')


