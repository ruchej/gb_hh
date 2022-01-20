from django.views.generic import ListView, DetailView
from .models import Article


class NewsList(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'news_list'
