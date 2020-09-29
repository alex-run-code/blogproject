from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
 path('posts/', views.PostList.as_view()),
 path('posts/<int:pk>', views.PostDetail.as_view()),
 path('posts/collections/<collection>/', views.PostCollectionList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)