from django.contrib import admin

from posts.models import Post, Group

admin.site.register(Post)
admin.site.register(Group)
