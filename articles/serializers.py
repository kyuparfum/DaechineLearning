from rest_framework import serializers
from .models import Article
# serializer는 전부 검색부분용 입니다. 
# 노래제목,가수, 해당 곡 앨범자켓 
class MusicSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()
    artist = serializers.SerializerMethodField()
    album = serializers.SerializerMethodField()
    id = serializers.CharField()

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
            'id': album.get('id'),
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
