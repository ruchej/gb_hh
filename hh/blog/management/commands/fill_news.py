from django.core.management.base import BaseCommand
from blog.models import Article


class Command(BaseCommand):
    def handle(self, *args, **options):
        news = Article.objects.create(title='News1', short_description='qweqwe', description='qweqweqwe',
                                      author='AuthorName')
