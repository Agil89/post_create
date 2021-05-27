from django.db import models
from django.contrib.auth import get_user_model
USER_MODEL = get_user_model()
# Create your models here.


class UsersLastRequest(models.Model):
    #relations
    user = models.ForeignKey(USER_MODEL,verbose_name='User',on_delete=models.CASCADE,db_index=True,related_name='last_request')

    #moderations
    last_request = models.DateTimeField()

    class Meta:
        verbose_name = 'UsersLastRequest'
        verbose_name_plural = 'UsersLastRequests'

        def __str__(self):
            return f'{self.user.username} last request was: {self.last_request}'

class Post(models.Model):
    #relations
    user =models.ForeignKey(USER_MODEL,verbose_name='User',on_delete=models.CASCADE,db_index=True)

    #informations
    my_post = models.CharField('Post',max_length = 500)
    likes = models.PositiveIntegerField(verbose_name='Like count',default=0)

    #moderations
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

        def __str__(self):
            return self.my_post



class Likes(models.Model):
    #relations
    user = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, related_name='liked_user',)
    post =models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_post', null=True, blank=True)

    #informations
    like = models.SmallIntegerField(default=0)

    # moderations
    like_added = models.DateField(format('%Y-%m-%d'), auto_now_add=True)


class Meta:
    verbose_name = 'Liked post'
    verbose_name_plural = 'Liked posts'

    def __str__(self):
        return f"{self.user.username} post: {self.post.my_post} "