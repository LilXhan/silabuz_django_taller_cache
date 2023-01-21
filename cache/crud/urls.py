from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateBook.as_view(), name='create'),
    path('delete/<int:id>', views.delete_book, name='delete'),
    path('<pk>/update', views.UpdateBook.as_view(), name='update')
]