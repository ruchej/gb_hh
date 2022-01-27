import random

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from accounts.models import UserStatus
from resumes import models as resumes_models
from vacancies import models as vacancies_models
from blog import models as blog_models
from recruiting import models as recruiting_models
from mixer.backend.django import mixer

User = get_user_model()


class Command(BaseCommand):
    help = 'Update database with test data.'

    @staticmethod
    def create_suser():
        if not User.objects.filter(username='suser').exists():
            User.objects.create_superuser('suser', 'suser@example.local', 'A1234567a')
        if not User.objects.filter(username='employer').exists():
            User.objects.create_superuser('employer', 'employer@employer.employer', 'A1234567a',
                                          status=UserStatus.EMPLOYER)
        if not User.objects.filter(username='employee').exists():
            User.objects.create_superuser('employee', 'employee@employee.employee', 'A1234567a',
                                          status=UserStatus.JOBSEEKER)

    @staticmethod
    def create_resumes():
        employee = User.objects.get(username='employee')
        mixer.blend(resumes_models.Resume, user=employee)
        for _ in range(random.randint(10, 100)):
            mixer.blend(resumes_models.Resume)

    @staticmethod
    def create_jobs():
        for _ in range(random.randint(10, 100)):
            mixer.blend(resumes_models.Job)
        resume = resumes_models.Resume.objects.filter(user__username='employee').first()
        mixer.blend(resumes_models.Job, experience=resume.experience)
        mixer.blend(resumes_models.Job, experience=resume.experience)

    @staticmethod
    def create_vacancies():
        for _ in range(random.randint(10, 100)):
            mixer.blend(vacancies_models.Vacancy)
        employer = User.objects.get(username='employer')
        mixer.blend(vacancies_models.Vacancy, employer=employer)

    @staticmethod
    def create_blog():
        for _ in range(random.randint(10, 100)):
            mixer.blend(blog_models.Article)

    @staticmethod
    def create_responses():
        for _ in range(random.randint(10, 100)):
            mixer.blend(recruiting_models.Response)
        employer = User.objects.get(username='employer')
        employee = User.objects.get(username='employee')
        mixer.blend(recruiting_models.Response, vacancy__employer=employer, resume__user=employee)

    @staticmethod
    def create_offers():
        for _ in range(random.randint(10, 100)):
            mixer.blend(recruiting_models.Offer)

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
            self.create_responses()
            self.create_offers()
            self.create_jobs()
        elif options.get('clear'):
            self.clear_db()
