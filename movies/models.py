from django.db import models
from accounts.models import User

# Create your models here.

class DayBoxOffice(models.Model) :
    date = models.TextField(primary_key=True)

class Genre(models.Model) :
    name = models.TextField()
    genre_id = models.IntegerField(primary_key=True)
    
class Movie(models.Model) :
    movie_id = models.IntegerField(primary_key=True)
    title_kr = models.TextField()
    title_en = models.TextField()
    poster_url = models.TextField()
    overview = models.TextField()
    dayboxoffice = models.ManyToManyField(DayBoxOffice,related_name='movies_day')
    genres = models.ManyToManyField(Genre, related_name ='movies')
    avgScore = models.FloatField(default=0.0)
    
class Image(models.Model) :
    imageUrl = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
class Video(models.Model) :
    videoUrl = models.TextField()
    title = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name = 'video_set')
    
class Actor(models.Model) :
    name = models.TextField()
    actor_id = models.IntegerField(primary_key=True)
    image_url = models.TextField()

class Casting(models.Model) :
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='casting_set')
    character = models.TextField()
    
class Score(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    score = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
