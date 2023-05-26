from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomTokenObtainPairSerializer, Userserializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from users.models import User
import speech_recognition as sr


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
    
class SoundAI (APIView):
    def post(self, request):
        audios=request.data['blob']
        Recognizer = sr.Recognizer()  # 인스턴스 생성
        mic = sr.AudioFile(audios)
        with mic as source:  # 안녕~이라고 말하면
            audio = Recognizer.listen(source)
        try:
            data = Recognizer.recognize_google(audio, language="ko")
        except:
            data=""

        print(data)  # 안녕 출력
        return Response({"message":data}, status=status.HTTP_200_OK)


#유사한 사람
