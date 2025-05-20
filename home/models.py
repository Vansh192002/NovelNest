from django.db import models    
from django.contrib.auth.models import User
from django.utils import timezone

genre_list = [('literature','Literature'),('romance', 'Romance'), ('thriller', 'Thriller'),('novel', 'Novel'),('fiction','Fiction'),('fantasy','Fantasy'),('mystery','Mystery')]

class Genre(models.Model):
    name = models.CharField(choices=genre_list ,blank=False,max_length=25)
    image = models.ImageField(upload_to='genre-thumbnails/')
    
    def __str__(self):
        return self.get_name_display()

class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    summary = models.TextField()
    publication_year = models.PositiveIntegerField()
    genres = models.ManyToManyField(Genre, related_name='books')
    pdf_file = models.FileField(upload_to='ebooks/')
    thumbnail = models.ImageField(upload_to='ebooks/thumbnails/', blank=True,null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=20,default="English")
    rating = models.SmallIntegerField(default=None)
    pages = models.IntegerField(default=None)
    
    def __str__(self):
        return f"{self.name} by {self.author}"
    
class ReadList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    read = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user','book')
    
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    favourite_genres = models.ManyToManyField(Genre,related_name='favorite_genres',blank=True) 
    profile_picture = models.ImageField(upload_to='profile_pics/',default='profile_pics/default.png')
    phone_number = models.CharField(max_length=15,unique=True, default=0)
    books_read = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}"


class Collection(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','book')    
    
    def __str__(self):
        return f"{self.user.username}'s Collection"        


