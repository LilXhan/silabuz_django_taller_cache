from django.db import models

# url = 'https://silabuzinc.github.io/books/books.json'

class Book(models.Model):

    title = models.CharField(max_length=400)
    authors = models.CharField(max_length=400)
    average_rating = models.FloatField()
    isbn = models.CharField(max_length=200)
    isbn13 = models.CharField(max_length=200)
    language_code = models.CharField(max_length=20)
    num_pages = models.IntegerField()
    ratings_count = models.IntegerField()
    text_reviews_count = models.IntegerField()
    publication_date = models.DateField()
    publisher = models.CharField(max_length=200)

    class Meta:
        db_table = 'books'