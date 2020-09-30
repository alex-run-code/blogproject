from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
 path('posts/', views.PostList.as_view()),
 path('posts/<int:pk>', views.PostDetail.as_view()),
 path('posts/collections/<collection>/', views.PostCollectionList.as_view()),
 path('posts/<post_id>/share/', views.post_share, name='post_share'),
 path('posts/<year>/<month>/<day>/<post>/', views.post_detail, name='post_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)