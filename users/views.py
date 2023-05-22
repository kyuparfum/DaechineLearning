from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomTokenObtainPairSerializer, Userserializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from users.models import User


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
        serializer = Userserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user # 요청받은 유저를 본래 유저로 넣고
            user.set_password(serializer.validated_data.get('password')) 
            user.username = serializer.validated_data.get('username')    
            user.save() # 저장    
            return Response({'message': '회원정보가 수정완료되었습니다!'}, status=status.HTTP_200_OK)
        
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class mockview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response("로그인되어있음!")