from django.urls import path
from .views import GetAnaliticData,UserCreateAPIView,login,PostLikeView,PostUnlikeView,PostCreateAPIView,UserInfoApiView
from rest_framework_simplejwt import views as jwt_views

app_name = 'api_account'

urlpatterns = [
    path('create/',UserCreateAPIView.as_view(),name='create-user'),
    path('login/',login),
    path('user-info/<int:pk>/',UserInfoApiView.as_view()),
    path('like/<int:id>/',PostLikeView),
    path('unlike/<int:id>/', PostUnlikeView),
    path('create-post/',PostCreateAPIView.as_view()),
    path('analitics/',GetAnaliticData.as_view(),name='analitic'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]