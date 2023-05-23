from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomTokenObtainPairSerializer, Userserializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from users.models import User

# from django.http import HttpResponseRedirect
# from rest_framework.permissions import AllowAny
# from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC


class Userview(APIView):
    def post(self, request):
      serializer = Userserializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"message":"!!회원가입완료!!"}, status=status.HTTP_201_CREATED)
      else:
        return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"message":"회원가입테스트"}, status=status.HTTP_201_CREATED)
    
    # 회원정보 수정(일부)
    def patch(self, request):
        if not request.user.is_authenticated:
                    return Response("로그인 먼저 해주세요", status=status.HTTP_401_UNAUTHORIZED)
        
        # 로그인되어있다면
        user = User.objects.get(id=request.user.id)
        user_serializer = Userserializer(user, data=request.data, partial=True)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save() # 저장    
            return Response({'message': '회원정보가 수정완료되었습니다!'}, status=status.HTTP_200_OK)
        
        else:
            return Response({"message":f"${user_serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class mockview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response("로그인되어있음!")
    
# 이메일 링크 열었을때
# class Activate(APIView):
    # def get(self, request, uidb64, token):
    #     try:
    #         uid = force_text(urlsafe_base64_decode(uidb64))
    #         user = Users.objects.get(pk=uid)
    #         user_dic = jwt.decode(token,SECRET_KEY,algorithm='HS256')
    #         if user.id == user_dic["user"]:
    #             user.is_active = True
    #             user.save()
    #             return redirect('http://127.0.0.1:8000/api/token/')

    #         return JsonResponse({'message':'auth fail'}, status=400)
    #     except ValidationError:
    #         return JsonResponse({'message':'type_error'}, status=400)
    #     except KeyError:
    #         return JsonResponse({'message':'INVALID_KEY'}, status=400)
    

# class ConfirmEmailView(APIView):
    # permission_classes = [AllowAny]

    # def get(self, *args, **kwargs):
    #     self.object = confirmation = self.get_object()
    #     confirmation.confirm(self.request)
    #     # A React Router Route will handle the failure scenario
    #     return HttpResponseRedirect('/') # 인증성공

    # def get_object(self, queryset=None):
    #     key = self.kwargs['key']
    #     email_confirmation = EmailConfirmationHMAC.from_key(key)
    #     if not email_confirmation:
    #         if queryset is None:
    #             queryset = self.get_queryset()
    #         try:
    #             email_confirmation = queryset.get(key=key.lower())
    #         except EmailConfirmation.DoesNotExist:
    #             # A React Router Route will handle the failure scenario
    #             return HttpResponseRedirect('/') # 인증실패
    #     return email_confirmation

    # def get_queryset(self):
    #     qs = EmailConfirmation.objects.all_valid()
    #     qs = qs.select_related("email_address__user")
    #     return qs