from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article
from .forms import ArticleCreateForm


class NewsList(ListView):
    model = Article
    context_object_name = 'news_list'
    extra_context = {'title': 'Новости'}
    paginate_by = 3

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
