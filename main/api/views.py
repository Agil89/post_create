from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView
from .serializers import LikeSerializer,UserSerializer,PostSerializer,UserInfoSerializer
from ..models import Likes,USER_MODEL,Post,UsersLastRequest
from django.http import HttpResponse
import json
import datetime
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.utils.timezone import now

from rest_framework.response import Response

from rest_framework.authtoken.models import Token

class UserCreateAPIView(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = USER_MODEL.objects.all()
    serializer_class = UserSerializer

class PostCreateAPIView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GetAnaliticData(ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        date_from = request.GET.get('date_from')
        first_date=datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
        date_to = request.GET.get('date_to')
        last_date = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()
        delta =last_date-first_date
        all_data = {}

        for x in range(delta.days):
            text_info = f"for date:{first_date + datetime.timedelta(days=x)}"
            like_count = len(Likes.objects.filter(
                like_added__range=[first_date + datetime.timedelta(days=x), first_date + datetime.timedelta(days=x)]))
            all_data[text_info] = like_count

        file_type = 'application/json'
        return HttpResponse(json.dumps(all_data), file_type)

class UserInfoApiView(RetrieveAPIView):
    queryset = USER_MODEL.objects.all()
    serializer_class = UserInfoSerializer
    lookup_field = 'user_id'

    def get(self, request,pk):
        user = USER_MODEL.objects.filter(id=pk).last()
        serializer = UserInfoSerializer(user)
        last_request=UsersLastRequest.objects.filter(user=user).last()
        return Response({
            'result': serializer.data,
            'last_request': last_request.last_request
        })

@csrf_exempt
@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)

    user = USER_MODEL.objects.get(username=username, password=password)
    if request.user.is_authenticated:
        print("user is authenticated")
    else:
        print("User is not authenticated")
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((permissions.IsAuthenticated,))
def PostLikeView(request,id):
    post_id = id
    print(post_id)
    post = Post.objects.get(id=post_id)
    if post:
        like = Likes.objects.filter(post=post, user=request.user).last()
        if like:
            if like.like == 0:
                post.likes += 1
                post.save()
            like.like = 1
            like.save()

        else:
            post.likes += 1
            post.save()
            Likes.objects.create(
                user=request.user,
                post=post,
                like=1,
            )
    return Response({'post like': 'Liked'})

@csrf_exempt
@api_view(["POST"])
@permission_classes((permissions.IsAuthenticated,))
def PostUnlikeView(request,id):
    post_id = id
    post = Post.objects.get(id=post_id)
    if post:
        like = Likes.objects.filter(post=post, user=request.user).last()
        if like:
            if like.like == 1:
                post.likes -= like.like
                post.save()
            like.delete()
        else:
            Likes.objects.create(
                user=request.user,
                post=post,
            )
    return Response({'post unlike': 'Unliked'})



class SetLastRequestMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            user = USER_MODEL.objects.filter(pk=request.user.pk).last()
            UsersLastRequest.objects.create(user=user,last_request=now())

        return response