from django.shortcuts import render
from .models import Post
from django.http import JsonResponse

# Create your views here.


def get_posts(requests):
    posts = Post.objects.all()
    data = {'results': list(posts.values('title', 'content', 'published'))}
    return JsonResponse(data)
