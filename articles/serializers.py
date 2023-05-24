from rest_framework import serializers
# serializer는 전부 검색부분용 입니다. 
# 노래제목,가수, 해당 곡 앨범자켓 
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