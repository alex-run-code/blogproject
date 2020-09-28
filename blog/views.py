from django.shortcuts import render
from .models import Post
from blog.models import Post
from blog.serializers import PostSerializer
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['status','author__username','publish','created']
    filter_backends = [DjangoFilterBackend]
    filter_fields = {
        'status': ['exact'],
        'author__username': ['exact'],
        'publish': ['gte', 'lte'],
        'created': ['gte', 'lte'],
        'category': ['exact'],
    }


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PublishedAfterFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)