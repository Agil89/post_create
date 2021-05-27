from django.contrib import admin
from .models import Post,Likes,UsersLastRequest




admin.site.register(Post)
admin.site.register(Likes)
admin.site.register(UsersLastRequest)

# Register your models here.
