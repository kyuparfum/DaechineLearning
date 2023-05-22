from rest_framework import serializers
from comments.models import Comment, Emoticon, EmoticonImages, UserBoughtEmoticon


# 댓글
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

# 이모티콘 이미지들
class EmoticonImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmoticonImages
        fields = ("id", "image",)

# 이모티콘
class EmoticonSerializer(serializers.ModelSerializer):
    images = EmoticonImagesSerializer(many=True, required=False)

    class Meta:
        model = Emoticon
        fields = "__all__"

# 유저가 가진 이모티콘
class UserBoughtEmoticonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBoughtEmoticon
        fields = "__all__"

