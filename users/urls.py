from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users import views

urlpatterns = [
    path('api/token/', views.CustomTokenObtainPairView.as_view(),name='token_obtain_pair'), #로그인-토큰받기
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   #토큰만료시 다시 갱신
    path('signup/', views.Userview.as_view()),  #회원가입
    path('mock/', views.mockview.as_view()),    #토큰유효확인
    path('profile/', views.Userview.as_view(), name='profile_edit'),    #회원정보 수정
]
