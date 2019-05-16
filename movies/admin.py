from django.contrib import admin
from .models import Movie,DayBoxOffice,Score,Genre,Image,Video,Actor
# Register your models here.

admin.site.register(Movie)
admin.site.register(DayBoxOffice)
admin.site.register(Score)
admin.site.register(Genre)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Actor)