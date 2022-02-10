from .models import Article


def recent_news(request):
    recent_news = Article.objects.all().order_by('-created_at')[:3]
    return {
        'recent_news': Article.objects.all().order_by('-created_at')[:3]
    }
