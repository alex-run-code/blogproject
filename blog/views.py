from django.shortcuts import render
from .models import Post
from blog.models import Post
from blog.serializers import PostSerializer
from rest_framework import generics


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


