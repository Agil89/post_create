from rest_framework import permissions
from django.views.generic import TemplateView,CreateView
from django.contrib.auth.views import LoginView
from .forms import LoginForm,AddPostForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from .models import Post,Likes
from django.http import HttpResponseRedirect

class MainPageView(TemplateView):
    template_name = 'index.html'

    permission_classes = [permissions.IsAuthenticated]
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        posts = Post.objects.all()
        context['posts']= posts
        return context


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request,'registration.html',{'form':form})

class AddPostView(LoginRequiredMixin,CreateView):
    form_class = AddPostForm
    template_name = 'create_post.html'
    success_url=reverse_lazy('home')

    def form_valid(self,form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)



def PostLikeView(request,pk):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
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
    return HttpResponseRedirect(reverse_lazy('home'))



def PostUnlikeView(request,pk):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
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
    return HttpResponseRedirect(reverse_lazy('home'))



# class DataInRangeForLikes(ListAPIView):
#     serializer_class = LikeSerializer
#
#     def get(self, request, *args, **kwargs):
#         likes_analitic = Like.objects.filter(like_published__range=[kwargs['date_from'], kwargs['date_to']])
#         if len(likes_analitic) > 0:
#             mimetype = 'application/json'
#             return HttpResponse(json.dumps({'likes by period': len(likes_analitic)}), mimetype)
#         else:
#             return self.list(request, *args, [{}])