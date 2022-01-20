from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article
from .forms import ArticleCreateForm


class NewsList(ListView):
    model = Article
    template_name = '../templates/article.html'
    context_object_name = 'news_list'
    extra_context = {'title': 'Новости'}
    paginate_by = 10


class CreatePost(CreateView):
    model = Article
    template_name = 'blog/create_post.html'
    form_class = ArticleCreateForm
    success_url = reverse_lazy('blog:news')


# class UpdatePost(UpdateView):
#     model = Article
#     template_name = 'blog/update_post.html'
#     success_url = reverse_lazy('blog:news')


def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")
