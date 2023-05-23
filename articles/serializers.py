from rest_framework import serializers
from articles.models import Article


class ArticleListSerializer (serializers.ModelSerializer):
    """ 포스팅된 게시글 메인으로 가져오기 """
    writer = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['writer', 'title', 'content', 'created_at', 'updated_at']

    # 작성자 필드 추가
    def get_writer(self, obj):
        return obj.writer.username


class ArticleCreateSerializer (serializers.ModelSerializer):
    """ 게시글 CRUD """
    class Meta:
        model = Article
        exclude = ['writer', 'created_at', 'updated_at', 'db_status']


class ArticleDetailSerializer (serializers.ModelSerializer):
    """ 게시글 상세 확인하기 """
    writer = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {'writer': {'read_only': True},
                        'created_at': {'read_only': True},
                        'updated_at': {'read_only': True},
                        }

    def get_writer(self, obj):
        return obj.writer.username
