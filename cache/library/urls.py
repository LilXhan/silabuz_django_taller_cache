from django.urls import path 
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    path('load/', views.LoadDataView.as_view(), name='load'),
    path('', cache_page(60*1500)(views.ListBookView.as_view()), name='index'),
    path('book/<int:id>', views.BookDetail.as_view(), name='select-book'),
    path('book/<int:id>/<str:author>', views.AuthorView.as_view(), name='authors'),
    path('books/list/10', cache_page(60*10)(views.GetBookQuery.as_view()), name='book-10')
]