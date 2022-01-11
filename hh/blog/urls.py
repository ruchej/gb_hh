from django.urls import path
from .views import NewsList, ShowPost

app_name = 'blog'

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('news/<int:post_id>/', ShowPost.as_view(), name='post'),
]
