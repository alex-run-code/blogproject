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

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


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


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    print(post)
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" \n\n{}\'s comments: {}'.format(post.title, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
        else:
            form = EmailPostForm()
        return render(request, 'blog/share.html', {'post': post, 'form': form, 'sent': sent})
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post': post, 'form': form})
