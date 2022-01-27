from django.urls import path
from .views import NewsList, CreatePost, DetailPost, UpdatePost, DeletePost

app_name = 'blog'

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('post-create/', CreatePost.as_view(), name='post_create'),
    path('post/<slug:post_slug>/', DetailPost.as_view(), name='post'),
    path('post-update/<slug:post_slug>/', UpdatePost.as_view(), name='post_update'),
    path('post-delete/<slug:post_slug>/', DeletePost.as_view(), name='post_delete'),
]
