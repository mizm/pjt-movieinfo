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
from .serializers import ScoreSerializer, MovieSerializer
# Create your views here.

def db_insert_movie(moviename) :
    try :
        tdic = Movie.objects.get(title_kr=moviename)
    except :
        tmurl = 'https://api.themoviedb.org/3/search/movie?api_key=8f03cc345840b05e82681223f1ff0d74&language=ko-KR&query={}&page=1&include_adult=false'.format(moviename)
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
v
@api_view(['GET'])
def get_comments(request,movie_id):
    movies = Movie.objects.get(pk=movie_id)
    comments = movie.score_set.all()
    serializer = ScoreSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_movie(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
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
        return Response({'message' : 'c'})
    except :
        return Response({'message':'error'})

def newmovie(request) :
    return render(request,'newmovie.html')
# 영화 리스트

def index(request) :
    movies = Movie.objects.all()
    comments = {}
    for i in movies :
        comments[i.movie_id] = i.score_set.all()
    # return render(request,'index.html')
    return render(request,'index.html',{'movies':movies,'comments':comments})

def boxoffice(request) :
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
            tdic = db_insert_movie(i)
            # print(tdic)
            t.movies_day.add(tdic)
            # break
    
    movies = t.movies_day.all()
    comments = {}
    for i in movies :
        comments[i.movie_id] = i.score_set.all()
    # return render(request,'index.html')
    return render(request,'index.html',{'movies':movies,'comments':comments})

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