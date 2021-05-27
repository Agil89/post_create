from rest_framework import serializers
from django.contrib.auth import get_user_model
USER_MODEL = get_user_model()
from rest_framework.authtoken.models import Token


from ..models import Post,Likes


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = (
            'username', 'password',
        )
    # def create(self, validated_data):
    #     user = super(UserSerializer, self).create(validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     token = Token.objects.get_or_create(user=user)
    #     return token



class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = (
            'last_login',
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id', 'my_post','likes',
        )


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = (
            'user', 'post', 'like', 'like_added'
        )


# class DislikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Dislike
#         fields = (
#             'dislike_user', 'dislike_post', 'dislike', 'dislike_published'
#         )


