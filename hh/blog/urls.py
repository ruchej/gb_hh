from django.urls import path
from .views import NewsList, CreatePost, show_post

app_name = 'blog'

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('post-create/', CreatePost.as_view(), name='post_create'),
    path('post/<int:post_id>/', show_post, name='post'),
]
