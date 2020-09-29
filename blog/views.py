from django.shortcuts import render
from .models import Post
from blog.models import Post, Collection
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
    }


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostCollectionList(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        print(self.kwargs['collection'])
        collection_tags = Collection.objects.values_list('tags__name', flat=True)
        return Post.objects.filter(tags__name__in=collection_tags).distinct()

