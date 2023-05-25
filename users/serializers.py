from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
    extra_kwargs = {
        'password': {'write_only': True},
    }

# 유저 회원가입 시리얼라이저
    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.is_active = False
        user.save()
        # print(f'validated_data : {validated_data}')
        return user

# 유저 정보수정 시리얼라이저
    def update(self, obj, validated_data):
        # print(f'obj : {obj}')
        # print(f'validated_data : {validated_data}')
        
        # obj에는 입력된 object가 담긴다.
        for key, value in validated_data.items():
            # print(key, value)
            if key == "password":
                obj.set_password(value)
                continue
            
            setattr(obj, key, value)
        obj.save()
        
        return obj

# 토큰 정보 커스터마이징
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        
        return token
