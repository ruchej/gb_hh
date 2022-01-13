from django.urls import path
from .views import NewsList

app_name = 'blog'

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
]
