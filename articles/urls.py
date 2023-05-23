from django.urls import path
from articles import views

urlpatterns = [
    path('', views.ArticleView.as_view(), name='article_main'),  # 메인 화면에 띄운다면
    path('<int:article_id>/', views.ArticleDetailView.as_view(),
         name='article_update'),  # 상세 게시글 crud
]
# path('<int:article_id>/', views.ArticleCreateSerializer.as_view(),
#      name='my_post_list_view'), 페이지 여럿 구성하지 않고
