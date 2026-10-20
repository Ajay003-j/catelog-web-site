from django.db import models
#from django.urls import reverse
from django.conf import settings
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, help_text='Enter a book genre')

    def __str__(self):
        return self.name
        
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    summary = models.TextField(max_length=1000, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.ManyToManyField(Genre)
    
    def __str__(self):
        return self.title

class Notes(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# class User(models.Model):
#     username = models.CharField(max_length=50,unique=True)
#     email = models.EmailField(max_length=50,unique=True)
#     password = models.CharField(max_length=254)

#     def __str__(self):
#         return self.username

