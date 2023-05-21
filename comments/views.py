from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from comments.serializers import CommentSerializer, EmoticonSerializer, EmoticonImagesSerializer
from comments.models import Comment, Emoticon, EmoticonImages, UserBoughtEmoticon


# Create your views here.

# music 댓글 가져오기
class CommentView(APIView):
    def get(self, request, article_id):
        comment = Comment.objects.filter(music=article_id)
        serializer = CommentSerializer(comment, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# 이모티콘 전부 다 가져오기
class EmoticonView(APIView):
    def get(self, request):
        emoticon = Emoticon.objects.all()
        serializer = EmoticonSerializer(emoticon, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

# 유저가 가진 이모티콘 가져오기
class UserBoughtEmoticonView(APIView):
    def get(self, request, user_id):
        emoticon_list = UserBoughtEmoticon.objects.filter(buyer=user_id)
        emoticons = []
        for a in emoticon_list:
            emoticons.append(a.emoticon)
        serializer = EmoticonSerializer(emoticons, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
