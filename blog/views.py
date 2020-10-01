from django.shortcuts import render, get_object_or_404
from blog.models import Post, Collection
from blog.serializers import PostSerializer
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .forms import EmailPostForm
from django.core.mail import send_mail
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.views.generic.edit import FormView
from django.contrib import messages
from django.db.models import Count



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

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    tags = post.tags.all()
    comments = post.comments.filter(active=True)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'tags': tags,
        'similar_posts': similar_posts,
    }
    return render(request, 'blog/detail.html', context)


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


class PostShare(FormView):
    template_name = 'blog/share.html'
    form_class = EmailPostForm
    success_url = '.'

    def get(self, request, *args, **kwargs):
        sent = False
        form = self.form_class(initial=self.initial)
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id, status='published')
        return render(request, self.template_name, {'form': form, 'post': post, 'sent': sent})

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form = self.form_class(initial=self.initial)
        cd = self.request.POST
        name = cd['name']
        email = cd['email']
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id, status='published')
        comments = cd['comments']
        to = cd['to']
        form.send_email(name, email, post, comments, to)
        messages.add_message(self.request, messages.INFO, 'Message sent to {} Bravo !'.format(to))
        return super().form_valid(form)



