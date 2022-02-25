from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
import feedparser

from el_pagination.views import AjaxListView

from .models import Article
from .forms import ArticleCreateForm


class NewsList(AjaxListView):
    model = Article
    context_object_name = 'news_list'
    page_template = 'blog/snippets/list/cards.html'

    def get_context_data(self, **kwargs):
        context = super(NewsList, self).get_context_data(**kwargs)
        context.update({'title': 'Новости'})
        return context

    def get_queryset(self):
        return Article.objects.filter(is_active=True)


class CreatePost(CreateView):
    model = Article
    form_class = ArticleCreateForm
    success_url = reverse_lazy('blog:news')


class UpdatePost(UpdateView):
    model = Article
    form_class = ArticleCreateForm
    slug_url_kwarg = 'post_slug'
    success_url = reverse_lazy('blog:news')
    template_name = 'blog/article_update.html'


class DeletePost(DeleteView):
    model = Article
    slug_url_kwarg = 'post_slug'
    success_url = reverse_lazy('blog:news')


class DetailPost(DetailView):
    model = Article
    slug_url_kwarg = 'post_slug'
    template_name = 'blog/article_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(DetailPost, self).get_context_data(**kwargs)
        context['title'] = context['post'].title
        return context


def rss_parser(request):
    url = 'https://lenta.ru/rss/top7'
    feeder = feedparser.parse(url)
    for entry in feeder['entries']:
        feed_title = entry.title
        link = entry.link
        context = {'feed_title': feed_title, 'link': link, }
        return render(request, 'snippets/recent_news.html', context)
