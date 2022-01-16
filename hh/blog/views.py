from django.views.generic import ListView, DetailView
from .models import Article


class NewsList(ListView):
    model = Article
    template_name = '../templates/article.html'
    context_object_name = 'news_list'
