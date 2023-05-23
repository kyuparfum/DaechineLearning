from rest_framework import serializers

class MusicSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField()
    artist = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get('name')

    def get_artist(self, obj):
        artists = obj.get('artists', [])
        if artists:
            return artists[0].get('name')
        else:
            return None
