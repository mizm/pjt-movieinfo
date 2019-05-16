from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/',views.detail_movie, name='detail'),
    path('boxoffice/', views.boxoffice, name='boxoffice'),
    path('newmovie/',views.newmovie, name='newmovie'),
    path('recommend/<int:movie_id>', views.recommend),
    path('similar/<int:movie_id>', views.similar),
    path('createmovie', views.createmovie, name='createmovie'),
    path('createscore', views.createscore, name='createscore'),
    path('get_movie/',views.get_movie),
    path('get_genre/',views.get_genre),
    path('get_boxoffice/',views.get_boxoffice),
    path('get_recommend/<int:movie_id>', views.get_recommend),
    path('get_similar/<int:movie_id>', views.get_similar),
    path('get_comments/<int:movie_id>',views.get_comments),
    path('delete/comment/<int:comment_id>',views.delete_comment),
    # path('<int:movie_id>/score/new',views.new_score, name='new_score'),
    # path('<int:movie_id>/score/<int:score_id>/delete/',views.delete_score, name='delete_score'),
    # path('<int:movie_id>/like/', views.like, name='like'),
]