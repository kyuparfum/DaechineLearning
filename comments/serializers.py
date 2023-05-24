from rest_framework import serializers
from comments.models import Comment, Emoticon, EmoticonImages, UserBoughtEmoticon


# 댓글
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

# 댓글 생성
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment', 'use_emoticon', 'music')

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

# 이모티콘 생성
class EmoticonCreateSerializer(serializers.ModelSerializer):
    images = EmoticonImagesSerializer(many=True, required=False)

    class Meta:
        model = Emoticon
        fields = "__all__"

    def create(self, validated_data):
        images_data = self.context.get('images', None)
        emoticon = super().create(validated_data)
        if images_data:
            for image_data in images_data:
                EmoticonImages.objects.create(emoticon=emoticon, image=image_data)
        return emoticon

# 유저가 가진 이모티콘
class UserBoughtEmoticonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBoughtEmoticon
        fields = "__all__"
