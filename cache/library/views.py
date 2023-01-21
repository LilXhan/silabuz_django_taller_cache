from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book

import urllib.request
import json


class GetBookQuery(LoginRequiredMixin, TemplateView):

    template_name = '10Books.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()[:10]

        return context

class AuthorView(LoginRequiredMixin, View):

    def get(self, request, id, author):

        context = {}

        if request.session['id'] == id:
            authors = request.session['authors']
            context['authors'] = authors
            return render(request, 'author.html', context)
        if author == 'author':
            try:
                book = Book.objects.get(pk=id)
                request.session['authors'] = book.authors
                request.session['id'] = book.id
                context['authors'] = book.authors
                return render(request, "author.html", context)
            except:
                return render(request, "author.html", context)
        else:
            return redirect('select-book', id=id)


class BookDetail(LoginRequiredMixin, View):

    def get(self, request, id):
        context = {}
        try:
            book = Book.objects.get(pk=id)
            request.session['authors'] = book.authors
            request.session['id'] = book.id
            context['book'] = book
            return render(request, "oneBook.html", context)
        except:
            return render(request, "oneBook.html", context)


class ListBookView(LoginRequiredMixin, View):
    
    def get(self, request):

        books = Book.objects.all()[:2]

        context = {
            'books': books
        }

        return render(request, 'index.html', context)



class LoadDataView(LoginRequiredMixin, View):
    def get(self, request):

        url = 'https://silabuzinc.github.io/books/books.json'

        data = urllib.request.urlopen(url)

        books = json.load(data)

        for book in books:
            book.pop('FIELD13')
            book.pop('bookID')

            book['authors'] = book['authors'][:400]

            try:
                book['average_rating'] = float(book['average_rating'])
            except:
                book['average_rating'] = 2.5
            
            try:
                book['num_pages'] = int(book['num_pages'])
            except:
                book['num_pages'] = 100

            
            book['publication_date'] = book['publication_date'].split('/')

            if '/'.join(book['publication_date']) in ['11/31/2000', '6/31/1982']:
                book['publication_date'] = '2023-1-20'
                b = Book.objects.create(**book)
                b.save()
                continue

            if len(book['publication_date']) == 3:
                date = '' #y-m-d
                date += book['publication_date'][2] + '-'
                date += book['publication_date'][0] +  '-'
                date += book['publication_date'][1]
            else:
                date = '2023-1-20'

            book['publication_date'] = date

            b = Book.objects.create(**book)
            b.save()

        return HttpResponse('cargado...')

