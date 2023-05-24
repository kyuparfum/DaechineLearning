from django.urls import path
from articles import views

urlpatterns = [
    path("music/api", views.MusicApiDetail.as_view(), name="music_api"),
    path("music/api/token", views.GetMusicAccessToken.as_view(),
         name="music_api_token"),
    path("music/api/search", views.MusicSearchApiDetail.as_view(),
         name="music_api_search"),
    path("music/api/genre", views.MusicGenreApiDetail.as_view(),
         name="music_api_genre"),
    # 메인 게시글 작성(POST), 불러오기(GET)
    path('', views.ArticleView.as_view(), name='article_main'),
    path('<int:article_id>/', views.ArticleDetailView.as_view(),
         name='article_detail'),  # 특정 게시글 불러와, 수정, 삭제(GET,PUT,DEL)
]
