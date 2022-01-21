import random

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from resumes import models as resumes_models
from vacancies import models as vacancies_models
from blog import models as blog_models
from mixer.backend.django import mixer

User = get_user_model()


class Command(BaseCommand):
    help = 'Update database with test data.'

    @staticmethod
    def create_suser():
        if not User.objects.filter(username='suser').exists():
            User.objects.create_superuser('suser', 'suser@example.local', 'A1234567a')

    @staticmethod
    def create_resumes():
        for _ in range(random.randint(10, 100)):
            mixer.blend(resumes_models.Resume)

    @staticmethod
    def create_vacancies():
        for _ in range(random.randint(10, 100)):
            mixer.blend(vacancies_models.Vacancy)

    @staticmethod
    def create_blog():
        for _ in range(random.randint(10, 100)):
            mixer.blend(blog_models.Article)

    @staticmethod
    def clear_db():
        User.objects.all().delete()
        resumes_models.Resume.objects.all().delete()
        vacancies_models.Vacancy.objects.all().delete()

    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            '--fill',
            action='store_true',
            default=False,
            help='Fill database.'
        )
        parser.add_argument(
            '-c',
            '--clear',
            action='store_true',
            default=False,
            help='Clear database.'
        )

    def handle(self, *args, **options):
        if options.get('fill'):
            self.create_suser()
            self.create_resumes()
            self.create_vacancies()
            self.create_blog()
        elif options.get('clear'):
            self.clear_db()
