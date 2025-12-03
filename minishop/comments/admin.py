from django.contrib import admin
from .models import *


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'grade']
    list_display_links = ['user']
    search_fields = ['user', 'text', 'grade']


class Comments_likes(admin.ModelAdmin):
    list_display = ['comment', 'user', 'likes', 'dislikes']
    list_display_links = ['comment', 'user', 'likes', 'dislikes']
    search_fields = ['comment', 'user']


admin.site.register(Comment_likes, Comments_likes)
admin.site.register(Comments, CommentsAdmin)