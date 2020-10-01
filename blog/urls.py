from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
 path('posts/', views.PostList.as_view()),
 path('posts/<int:pk>/', views.PostDetail.as_view()),
 path('posts/collections/<collection>/', views.PostCollectionList.as_view()),
 path('posts/<post_id>/share/', views.PostShare.as_view(), name='post_share'),
 path('posts/<slug>/', views.post_detail, name='post_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)