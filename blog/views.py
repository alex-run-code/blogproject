from django.shortcuts import render
from .models import Post
from django.http import JsonResponse

# Create your views here.


def get_posts(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'blog/list.html', context)

def get_post_by_slug(request, url_slug):
    slug = url_slug
    post = Post.objects.filter(slug=slug).first()
    context = {'post':post}
    return render(request, 'blog/post.html', context)


