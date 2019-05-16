from django.shortcuts import render, redirect, get_object_or_404
from bs4 import BeautifulSoup
from selenium import webdriver
import requests, datetime
from .models import DayBoxOffice, Movie, Score, Genre, Image, Video, Actor, Casting
from accounts.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .forms import ScoreForm
from django.contrib.auth.decorators import login_required
from .serializers import ScoreSerializer, MovieSerializer, GenreSerializer
# Create your views here.

def db_insert_movie(moviename) :
    try :
        tdic = Movie.objects.get(title_kr=moviename)
    except :
        tmurl = 'https://api.themoviedb.org/3/search/movie?api_key=8f03cc345840b05e82681223f1ff0d74&language=ko-KR&query={}&page=1&include_adult=false'.format(moviename)
        print(tmurl)
        results = requests.get(tmurl).json()['results'][0]
        movie_id = results['id']
        overview = results['overview']
        title_kr = results['title']
        title_en = results['original_title']
        poster_url = 'https://image.tmdb.org/t/p/original'+results['poster_path']
        tdic = Movie(
            movie_id = movie_id,
            title_kr = title_kr,
            title_en = title_en,
            poster_url = poster_url,
            overview = overview,
            avgScore = 0.0,
            )
        tdic.save()
        for i in results['genre_ids'] :
            tdic.genres.add(i)
        c = Image(imageUrl = 'https://image.tmdb.org/t/p/original/'+results['backdrop_path'],movie=tdic)
        tmurl = 'https://api.themoviedb.org/3/movie/{}/credits?api_key=8f03cc345840b05e82681223f1ff0d74'.format(movie_id)
        results = requests.get(tmurl).json()["cast"]
        i = 0
        for k in results :
            try :
                actor = Actor.objects.get(actor_id=results['id'])
            except :
                try :
                    actor = Actor(actor_id=k['id'],name=k['name'],image_url='https://image.tmdb.org/t/p/original/'+k['profile_path'])
                    actor.save()
                except :
                    continue
            character = k['character']
            try:
                c = Casting(actor = actor, movie = tdic, character=character)
                c.save()
            except :
                continue
        tmurl = 'https://api.themoviedb.org/3/movie/{}/videos?api_key=8f03cc345840b05e82681223f1ff0d74&language=ko-KR'.format(movie_id)
        results = requests.get(tmurl).json()["results"]
        for k in results :
            video = Video(videoUrl = 'https://www.youtube.com/embed/'+k['key'],title = k['name'], movie = tdic)
            video.save()
        # kourl = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
        # koprams = {
        #     'key' : 'f6bf3bb38f6afc47e0622a5d9303370b',
        #     'movieCd' : i['movieCd']
        # }
        # res = requests.get(kourl,params=koprams).json()['movieInfoResult']['movieInfo']
       
        # n_url = 'https://openapi.naver.com/v1/search/movie.json'
        # headers = { 'X-Naver-Client-Id' : 'nDBEUg5j49uc6iATE_6U' , 'X-Naver-Client-Secret': 'PDzctGCKhu' }
        # naparams = {
        #     'query' : res['movieNm']
        # }
        # resq = requests.get(n_url,params=naparams,headers=headers).json()['items'][0]
        # linkk = resq['link']
        # image = 'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode='+linkk.split('=')[1]
        # source = requests.get(image).text
        # soup = BeautifulSoup(source, 'html.parser')
        # image_url = soup.select('#targetImage')[0].get('src')
        
        # tdic = Movie(movie_id = res['movieCd'],
        #     title_kr = res['movieNm'],
        #     title_en = res['movieNmEn'],
        #     poster_url = image_url,
        #     link_url=linkk
        #     )
        # 
        # tdic.save()
    return tdic
@api_view(['GET'])
def delete_comment(request,comment_id) :
    comment = Score.objects.get(pk=comment_id)
    comment.delete()
    return Response({'message':'success'})
    
@api_view(['GET'])
def get_comments(request,movie_id):
    movies = Movie.objects.get(pk=movie_id)
    comments = movie.score_set.all()
    serializer = ScoreSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_movie(request):
    movies = Movie.objects.all().order_by('-avgScore')
    
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
def get_genre(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createmovie(request):
    i = request.data
    try :
        movie = Movie.objects.get(movie_id=i['id'])
        return Response({'message' : 'Already Exist!'})
    except :
        db_insert_movie(i['title'])
        return Response({'message':'complete'})

def recommend(request,movie_id) :
    return render(request,'index.html',{'point':2,'movie_id':movie_id})
    
@api_view(['GET'])
def get_recommend(request,movie_id) :
    tmurl = 'https://api.themoviedb.org/3/movie/'+str(movie_id)+'/recommendations?api_key=8f03cc345840b05e82681223f1ff0d74&language=ko-KR&page=1'
    result = requests.get(tmurl).json()['results']
    movies = []
    for i in result :
        try :
            movies.append(db_insert_movie(i['title']))
        except :
            continue
    serializer = MovieSerializer(movies, many=True)
    print(movies)
    return Response(serializer.data)
def similar(request,movie_id) :
    return render(request,'index.html',{'point':3,'movie_id':movie_id})
    
@api_view(['GET'])
def get_similar(request,movie_id) :
    tmurl = 'https://api.themoviedb.org/3/movie/'+str(movie_id)+'/similar?api_key=8f03cc345840b05e82681223f1ff0d74&language=ko-KR&page=1'
    result = requests.get(tmurl).json()['results']
    movies = []
    for i in result :
        try :
            movies.append(db_insert_movie(i['title']))
        except :
            continue
    serializer = MovieSerializer(movies, many=True)
    print(movies)
    return Response(serializer.data)
    
@login_required
@api_view(['POST'])
def createscore(request):
    i = request.data
    print(i)
    try :
        movie = Movie.objects.get(pk=i['movie'])
        user = User.objects.get(pk=i['user_id'])
        content = i['content']
        score = i['score']
        c = Score(movie=movie,user=user,content=content,score=score)
        c.save()
        return Response({'message' : c.pk })
    except :
        return Response({'message':'error'})

def newmovie(request) :
    return render(request,'newmovie.html')
# 영화 리스트

def index(request) :
    movies = Movie.objects.all()
    for i in movies :
        k = 0
        s = 0
        for j in i.score_set.all() :
            k+=1
            s+=j.score
        if k > 0 :
            i.avgScore = round(s/k,2)
            i.save()
    return render(request,'index.html',{'point':0})
    
def boxoffice(request) :
    return render(request, 'index.html',{'point':1})
    
@api_view(['GET'])
def get_boxoffice(request) :
    # tmurl = 'https://api.themoviedb.org/3/genre/movie/list?api_key=8f03cc345840b05e82681223f1ff0d74&language=ko-KR'
    # result = requests.get(tmurl).json()['genres']
    # for i in result :
    #     genre = Genre(genre_id = i['id'], name = i['name'])
    #     genre.save()
    # genre save 끝
    # # detail_movie(299534)
    
    dt = datetime.datetime.now() - datetime.timedelta(days=1)
    dt1 = dt.strftime('%Y-%m-%d')
    dt2 = dt.strftime('%Y%m%d')
    movies = []

    # t = DayBoxOffice(pk=1)
    # t.delete()
    try :
        t = DayBoxOffice.objects.get(date=dt1)
    except :
        t = DayBoxOffice(date=dt1)
        t.save()
        url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
        params = {
            'key' : 'f6bf3bb38f6afc47e0622a5d9303370b',
            'targetDt' : dt2
        }
        res = requests.get(url,params=params).json()
        for i in res["boxOfficeResult"]["dailyBoxOfficeList"] :
            movies.append(i['movieCd'])
            try :
                tdic = db_insert_movie(i['movieNm'])
            # print(tdic)
                t.movies_day.add(tdic)
            except :
                continue
            # break
    
    movies = t.movies_day.all()
    serializer = MovieSerializer(movies, many=True)
    print(movies)
    return Response(serializer.data)
    # return render(request,'index.html')

def detail_movie(request,movie_id) :
    movie = Movie.objects.get(movie_id=movie_id)
    actors = []
    k = 0
    for i in movie.casting_set.all() :
        k+=1
        if k > 5 :
            break
        actors.append(i)
    # for i in movie.casting_set.all() :
    #     print(i.character)
    return render(request,'detail.html',{'movie':movie,'actors':actors})
    # return 
    
# # 리뷰와 평점
# @login_required
# def new_score(request, movie_id):
#     movie = Movie.objects.get(id=movie_id)
#     score_form = ScoreForm(request.POST)
#     if request.user.is_authenticated:
#         if score_form.is_valid():
#             score = score_form.save(commit=False)
#             score.movie = movie
#             score.user = request.user
#             score.save()
#     return redirect('', movie_id)

# # 리뷰 삭제
# @login_required
# def delete_score(request, movie_id, score_id):
#     score = Score.objects.get(id=score_id)
#     if request.user.is_authenticated:
#         if score.user == request.user:
#             score.delete()
#         return redirect('', movie_id)
        
# # 좋아요
# @login_required
# def like(request, movie_id):
#     movie = get_object_or_404(Movie, id=movie_id)
    
#     if request.user in movie.like_users.all():
#         # 좋아요 취소
#         movie.like_users.remove(request.user)
#         liked = False 
#     else:
#         # 좋아요
#         movie.like_users.add(request.user)
#         liked = True
#     return redirect('')