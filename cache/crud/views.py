from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import F

from .forms import BookForm
from library.models import Book

from django.views.generic import View
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def delete_book(request, id):
    b = Book.objects.get(pk=id)
    b.delete()
    return redirect('index')

class UpdateBook(LoginRequiredMixin, UpdateView):
    model = Book 
    template_name = 'book_update_form.html'

    fields = [
        'title',
        'publisher',
        'authors'
    ]

    success_url = reverse_lazy('index')


class CreateBook(LoginRequiredMixin, View):

    def get(self, request):    
        form = BookForm

        context = {
            'form': form 
        }

        return render(request, 'create.html', context)

    def post(self, request):

        form = BookForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            b = Book.objects.create(**cleaned_data)
            b.save()

            return redirect('index')