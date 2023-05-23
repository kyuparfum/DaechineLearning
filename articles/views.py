from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from articles.models import Article
from articles.serializers import (
    ArticleListSerializer,
    ArticleCreateSerializer,
    ArticleDetailSerializer,
)
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class ArticleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ GET 요청 시 포스팅된 모든 게시글 불러옵니다. many = True 필요 """
        post = Article.objects.all()
        serializer = ArticleListSerializer(post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """ POST 요청 시 로그인 유저만 게시글을 작성합니다 """
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(writer=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, article_id):
        """ GET 요청 시 특정 게시글을 가져옵니다 """
        post = get_object_or_404(Article, id=article_id)
        serializer = ArticleDetailSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, article_id):
        """ PUT 요청 시 특정 게시글을 수정합니다. """
        post = get_object_or_404(Article, id=article_id)

        if post.writer != request.user:
            return Response({"message": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleCreateSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, article_id):
        """ DELETE 요청 시 특정 게시글 삭제 """
        post = get_object_or_404(Article, id=article_id, db_status=1)

        if post.writer != request.user:
            return Response({"message": "삭제 권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)
        else:
            post.db_status = 2
            post.save()
            return Response({"message": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
