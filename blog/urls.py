from django.urls import path
from . import views

urlpatterns = [
 path('posts/', views.get_posts, name='posts'),
 path('posts/<str:url_slug>', views.get_post_by_slug, name='get_post_by_slug')
]