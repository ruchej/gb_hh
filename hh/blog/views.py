from django.views.generic import ListView, DetailView
from .models import Article


class NewsList(ListView):
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'news_list'


class ShowPost(DetailView):
    model = Article
    template_name = 'blog/post.html'
    context_object_name = 'post'
