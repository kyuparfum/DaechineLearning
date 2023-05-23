from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# 구글 소셜 로그인
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView

# from dj_rest_auth.registration.views import VerifyEmailView

from users import views

urlpatterns = [
    path('api/token/', views.CustomTokenObtainPairView.as_view(),name='token_obtain_pair'), #로그인-토큰받기
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   #토큰만료시 다시 갱신
    path('signup/', views.Userview.as_view()),  #회원가입
    path('mock/', views.mockview.as_view()),    #토큰유효확인
    path('profile/', views.Userview.as_view(), name='profile_edit'),    #회원정보 수정
    
    # 구글 소셜로그인
    # path('google/login', google_login, name='google_login'),
    # path('google/callback/', google_callback, name='google_callback'),
    # path('google/login/finish/', GoogleLogin.as_view(), name='google_login_todjango'),
    

    # 일반 회원 회원가입/로그인
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # # 유효한 이메일이 유저에게 전달
    # re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # # 유저가 클릭한 이메일(=링크) 확인
    # re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', views.ConfirmEmailView.as_view(), name='account_confirm_email'),

]
