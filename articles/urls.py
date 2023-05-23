from django.contrib import admin
from django.urls import path
from articles import views

urlpatterns = [
    # path('/', admin.site.urls),
    path("music/api", views.MusicApiDetail.as_view(), name="music_api"),
    path("music/api/token", views.GetMusicAccessToken.as_view(), name="music_api_token"),
    path("music/api/search", views.MusicSearchApiDetail.as_view(),name="music_api_search"),
    path("music/api/genre", views.MusicGenreApiDetail.as_view(),name="music_api_genre"),
]
