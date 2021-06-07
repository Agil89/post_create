from django.urls import path
from .views import MainPageView,CustomLoginView,register,AddPostView,PostLikeView,PostUnlikeView
from django.contrib.auth.views import LogoutView


urlpatterns=[
    path('', MainPageView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/',register,name='register'),
    path('add/',AddPostView.as_view(),name='add'),
    path('like/<int:pk>/',PostLikeView,name='like'),
    path('unlike/<int:pk>/',PostUnlikeView,name='unlike')

]