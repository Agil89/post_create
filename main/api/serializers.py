from rest_framework import serializers
from django.contrib.auth import get_user_model
USER_MODEL = get_user_model()

from ..models import Post,Likes


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = (
            'username', 'password',
        )


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



