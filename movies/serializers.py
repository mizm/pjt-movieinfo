from rest_framework import serializers
from .models import Score, Movie, Genre
from accounts.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name',]

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_id','name']

class ScoreSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = Score
        fields = ['id','username','score','content']

class MovieSerializer(serializers.ModelSerializer):
    score_set = ScoreSerializer(many=True)
    genres = GenreSerializer(many=True)
    class Meta :
        model = Movie
        fields = ['movie_id','title_kr','title_en','poster_url','overview','score_set','avgScore','genres']
    