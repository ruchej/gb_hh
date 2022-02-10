import random

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from cities_light.models import Country
from cities_light.models import City

from accounts.models import UserStatus, Employer, JobSeeker
from resumes import models as resumes_models
from vacancies import models as vacancies_models
from blog import models as blog_models
from recruiting import models as recruiting_models
from mixer.backend.django import mixer

User = get_user_model()

russia = Country.objects.get(name='Russia')
moscow = City.objects.get(name='Moscow')
st_peter = City.objects.get(name='Saint Petersburg')
chelyabinsk = City.objects.get(name='Chelyabinsk')


class Command(BaseCommand):
    help = 'Update database with test data.'

    @staticmethod
    def create_suser():
        if not User.objects.filter(username='suser').exists():
            User.objects.create_superuser('suser', 'suser@example.local', 'A1234567a',
                                          status=UserStatus.MODERATOR)
        if not User.objects.filter(username='employer').exists():
            employer = User.objects.create_superuser('employer', 'employer@employer.employer', 'A1234567a',
                                                     status=UserStatus.EMPLOYER)
            Employer.objects.get(user=employer).delete()
            mixer.blend(Employer, user=employer, name='Google', description=mixer.RANDOM,
                        phone=mixer.RANDOM, country=russia, city=moscow)
            mixer.blend(vacancies_models.Vacancy, employer=employer,
                        title='Python Developer', description='Разработчик на питоне (Django)',
                        hashtags='Python, Django', salary='500000')
        else:
            employer = User.objects.get(username='employer')

        if not User.objects.filter(username='employee').exists():
            employee = User.objects.create_superuser('employee', 'employee@employee.employee', 'A1234567a',
                                                     status=UserStatus.JOBSEEKER)
            JobSeeker.objects.get(user=employee).delete()
            mixer.blend(JobSeeker, user=employee, first_name='Василий', patronymic='Васильевич',
                        last_name='Пупкин', date_birth=mixer.RANDOM, sex=JobSeeker.Sex.MAN,
                        country=russia, city=moscow)
            resume = mixer.blend(resumes_models.Resume, user=employee)
            mixer.cycle(5).blend(resumes_models.Job, experience=resume.experience)
        else:
            employee = User.objects.get(username='employee')
        mixer.blend(recruiting_models.Response, vacancy__employer=employer, resume__user=employee)

    @staticmethod
    def create_users():
        for _ in range(random.randint(10, 20)):
            user = mixer.blend(User, status=random.choice([UserStatus.JOBSEEKER, UserStatus.EMPLOYER]))
            if user.status == UserStatus.JOBSEEKER:
                JobSeeker.objects.get(user=user).delete()
                mixer.blend(JobSeeker, user=user, date_birth=mixer.RANDOM,
                            sex=random.choice([JobSeeker.Sex.MAN, JobSeeker.Sex.WOMAN]),
                            country=russia,
                            city=random.choice([moscow, st_peter, chelyabinsk]))
            elif user.status == UserStatus.EMPLOYER:
                Employer.objects.get(user=user).delete()
                mixer.blend(Employer, user=user, name=mixer.RANDOM, description=mixer.RANDOM,
                            phone=mixer.RANDOM, country=russia,
                            city=random.choice([moscow, st_peter, chelyabinsk]))

    @staticmethod
    def create_resumes():
        for _ in range(random.randint(10, 100)):
            mixer.blend(resumes_models.Resume, user=mixer.SELECT,
                        user__status=UserStatus.JOBSEEKER)

    @staticmethod
    def create_jobs():
        for _ in range(random.randint(10, 100)):
            mixer.blend(resumes_models.Job, experience=mixer.SELECT)

    @staticmethod
    def create_vacancies():
        for _ in range(random.randint(10, 100)):
            mixer.blend(vacancies_models.Vacancy, employer=mixer.SELECT,
                        employer__status=UserStatus.EMPLOYER, description=mixer.RANDOM,
                        hashtags=mixer.RANDOM)

    @staticmethod
    def create_blog():
        for _ in range(random.randint(10, 100)):
            mixer.blend(blog_models.Article)

    @staticmethod
    def create_responses():
        for _ in range(random.randint(10, 100)):
            mixer.blend(recruiting_models.Response, vacancy=mixer.SELECT, resume=mixer.SELECT)

    @staticmethod
    def create_offers():
        for _ in range(random.randint(10, 100)):
            mixer.blend(recruiting_models.Offer, vacancy=mixer.SELECT, resume=mixer.SELECT)

    @staticmethod
    def clear_db():
        recruiting_models.Offer.objects.all().delete()
        recruiting_models.Response.objects.all().delete()
        resumes_models.Resume.objects.all().delete()
        vacancies_models.Vacancy.objects.all().delete()
        Employer.objects.all().delete()
        JobSeeker.objects.all().delete()
        User.objects.all().delete()
        blog_models.Article.objects.all().delete()

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
            self.create_users()
            self.create_resumes()
            self.create_jobs()
            self.create_vacancies()
            self.create_blog()
            self.create_responses()
            self.create_offers()
        elif options.get('clear'):
            self.clear_db()
