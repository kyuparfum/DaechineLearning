from django.urls import path
from articles import views

urlpatterns = [
    path('', views.ArticleView.as_view(),
         name='article_main'),  # 메인 게시글 작성(POST), 불러오기(GET)
    path('<int:article_id>/', views.ArticleDetailView.as_view(),
         name='article_detail'),  # 특정 게시글 불러와, 수정, 삭제(GET,PUT,DEL)
]
