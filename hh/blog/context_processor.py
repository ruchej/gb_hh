from .models import Article


def recent_news(request):
    return {
        'recent_news': Article.objects.filter(is_active=True)[:3]
    }
