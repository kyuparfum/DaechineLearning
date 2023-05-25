from rest_framework import serializers
from articles.models import Article


class MusicSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()
    artist = serializers.SerializerMethodField()
    album = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get('name')

    def get_artist(self, obj):
        artists = obj.get('artists', [])
        if artists:
            return artists[0].get('name')
        else:
            return None

    def get_album(self, obj):
        album = obj.get('album', {})
        return {
            'name': album.get('name'),
            'release_date': album.get('release_date'),
            'images': album.get('images'),
            'artist_name': album.get('artists', [{}])[0].get('name'),
        }


class ImageSerializer(serializers.Serializer):
    url = serializers.URLField()
    width = serializers.IntegerField()
    height = serializers.IntegerField()


class ArtistSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    href = serializers.CharField()
    images = ImageSerializer(many=True, required=False, read_only=True)


class ArticleListSerializer (serializers.ModelSerializer):
    """ 게시글 직렬화 """
    # writer = serializers.SerializerMethodField()


    class Meta:
        model = Article
        fields = ['id', 'writer', 'title', 'content', 'created_at', 'updated_at']

    # 작성자 필드 추가
    # def get_writer(self, obj):
    #     return obj.writer.username


class ArticleCreateSerializer (serializers.ModelSerializer):
    """ 생성, 수정 게시글 데이터 직렬화 """
    class Meta:
        model = Article
        exclude = ['id', 'writer', 'db_status']
        # fields = ['title', 'content']


class ArticleDetailSerializer (serializers.ModelSerializer):
    """ 상세 게시글 직렬화 """
    # writer = serializers.SerializerMethodField() # 불필요

    class Meta:
        model = Article
        fields = '__all__'
        # extra_kwargs = {'writer_id': {'read_only': True}, # 불필요
        #                 'writer': {'read_only': True},
        #                 'created_at': {'read_only': True},
        #                 'updated_at': {'read_only': True},
        #                 }

    # def get_writer(self, obj): # 불필요
    #     return obj.writer.username