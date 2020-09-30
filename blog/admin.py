from django.contrib import admin
from .models import Post, Collection, Comment
# Register your models here.

admin.site.register(Post)
admin.site.register(Collection)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

admin.site.register(Comment, CommentAdmin)