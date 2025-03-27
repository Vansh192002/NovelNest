from django.db import models    
from django.contrib.auth.models import User
from django.utils import timezone

genre_list = [('literature','Literature'),('romance', 'Romance'), ('thriller', 'Thriller'),('novel', 'Novel'),('fiction','Fiction'),('fantasy','Fantasy'),('mystery','Mystery')]

class Genre(models.Model):
    name = models.CharField(choices=genre_list ,blank=True,max_length=25)
    image = models.ImageField(upload_to='genre-thumbnails/')

class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    summary = models.TextField()
    publication_year = models.DateField(max_length=100)
    genres = models.ManyToManyField(Genre, related_name='books')
    pdf_file = models.FileField(upload_to='ebooks/')
    thumbnail = models.ImageField(upload_to='ebooks/thumbnails/', blank=True,null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    
class ReadList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    read = models.DateTimeField(default=timezone.now)
    
class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    favourite_genres = models.ManyToManyField(Genre,related_name='favorite_genres',blank=True) 
    books_read = models.PositiveIntegerField(default=0)

class Collection(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(choices=[('TBR','TO READ'),('Reading', 'Currently Reading'), ('Read', 'Read')],blank=True,max_length=25)
    added_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','book')    
        


