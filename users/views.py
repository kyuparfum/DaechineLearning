from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomTokenObtainPairSerializer, Userserializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from users.models import User,UserActiveArticle
from articles.models import MusicGenreTable
import speech_recognition as sr
import math


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
users=User.objects.all().values_list("id")
users=list(set(users))
user_genre={1: {'acoustic': 0.1, 'afrobeat': 10, 'alt-rock': 10}, 3: {'acoustic': 12, 'afrobeat': 13, 'alt-rock': 11}}
for user in users:
    print(user[0])
    datas=UserActiveArticle.objects.filter(user=user[0],listen_rate__gt=0.1,created_at__range=["2023-05-26","2023-05-27"]).order_by("user")

    genre_dic=user_genre.get(user[0],{})
    #기존 데이터 0.9배
    for genre in genre_dic:
        genre_dic[genre]*=0.9

    #추가데이터
    for data in datas:
        genres=MusicGenreTable.objects.filter(music=data.article)
        print(genres)
        for genre in genres:
            print(genre.genre.name)
            genre_dic[genre.genre.name]=genre_dic.get(genre.genre.name,0)+1
            pass
    if genre_dic!={}:
        user_genre[user[0]]=genre_dic
    print("~~~~~~~~~~~~~~~~~~~~~")

print(user_genre)

def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

users=combinations(user_genre, 2)  # 조합

point_dic={}

#취향벡터의 길이
user_len_dic={}
for user_name in user_genre:
    user_len_dic[user_name]=0
    for n in user_genre[user_name].values():
        user_len_dic[user_name]+=n*n
    user_len_dic[user_name]=math.sqrt(user_len_dic[user_name])




#유사정도 측정
for user_1,user_2 in users:
    point_dic[(user_1,user_2)]=0
    if user_1 < user_2:
        small_genre=user_genre[user_1]
    else:
        small_genre=user_genre[user_2]

    for genre_love in small_genre:

        point_dic[(user_1,user_2)]+=user_genre[user_1].get(genre_love,0)*user_genre[user_2].get(genre_love,0)\
                                /user_len_dic[user_1]/user_len_dic[user_2]
#최대인사람 5명 뽑기
similar_users={}
sorted_dict = sorted(point_dic.items(), key = lambda item: item[1],reverse= True)

for user_name in user_genre:
    similar_users[user_name]=[]

for (user1,user2),similar_rate in sorted_dict:
    if len(similar_users[user1])<5:
        similar_users[user1]+=[user2]
    if len(similar_users[user2])<5:
        similar_users[user2]+=[user1]
print(similar_users)