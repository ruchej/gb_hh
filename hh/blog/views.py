from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article
from .forms import ArticleCreateForm


class NewsList(ListView):
    model = Article
    context_object_name = 'news_list'
    extra_context = {'title': 'Новости'}
    paginate_by = 3


class CreatePost(CreateView):
    model = Article
    form_class = ArticleCreateForm
    success_url = reverse_lazy('blog:news')


class UpdatePost(UpdateView):
    model = Article
    form_class = ArticleCreateForm
    slug_url_kwarg = 'post_slug'
    success_url = reverse_lazy('blog:news')


class DeletePost(DeleteView):
    model = Article
    slug_url_kwarg = 'post_slug'
    success_url = reverse_lazy('blog:news')


def show_post(request, post_slug):
    return HttpResponse(f"Отображение статьи с slug = {post_slug}")
