import json
import random

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from cities_light.models import Country
from cities_light.models import City

from accounts.models import Employer, JobSeeker
from conf.choices import PublicStatusChoices, SexChoices, UserStatusChoices
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


def get_random_phone():
    n = '0000000000'
    while '9' in n[3:6] or n[3:6] == '000' or n[6] == n[7] == n[8] == n[9]:
        n = str(random.randint(10 ** 9, 10 ** 10 - 1))
    return '+' + n[:3] + '-' + n[3:6] + '-' + n[6:]


class Command(BaseCommand):
    help = 'Update database with test data.'
    employers_fixtures = []
    vacancies_fixtures = []
    news_fixtures = []

    @staticmethod
    def create_suser():
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'suser@example.local', 'admin',
                                          status=UserStatusChoices.MODERATOR)
        if not User.objects.filter(username='employer').exists():
            employer = User.objects.create_superuser('employer', 'employer@employer.employer', 'A1234567a',
                                                     status=UserStatusChoices.EMPLOYER)
            Employer.objects.get(user=employer).delete()
            mixer.blend(Employer, user=employer, name='Google', description=mixer.RANDOM,
                        phone=get_random_phone(), country=russia, city=moscow)
            employer.avatar = 'avatars/google-logo.webp'
            employer.save()
            mixer.blend(vacancies_models.Vacancy, employer=employer,
                        title='Python Developer', description='Разработчик на питоне (Django)',
                        hashtags='Python, Django', salary='500000 руб')
            mixer.blend(vacancies_models.Vacancy, employer=employer,
                        title='JavaScript Developer', description='JS разработчик (React)',
                        hashtags='JavaScript, React', salary='5000 руб')
            mixer.blend(vacancies_models.Vacancy, employer=employer,
                        title='Embedded Software Developer', description='Разработчик встраиваемых систем',
                        hashtags='C, RTOS, AUTOSAR', salary='500 руб')
        else:
            employer = User.objects.get(username='employer')

        if not User.objects.filter(username='employee').exists():
            employee = User.objects.create_superuser('employee', 'employee@employee.employee', 'A1234567a',
                                                     status=UserStatusChoices.JOBSEEKER)
            JobSeeker.objects.get(user=employee).delete()
            mixer.blend(JobSeeker, user=employee, first_name='Василий', patronymic='Васильевич',
                        last_name='Пупкин', date_birth=mixer.RANDOM, sex=SexChoices.MAN,
                        country=russia, city=moscow, phone=get_random_phone())
            employee.avatar = 'avatars/pupkin.jpg'
            employee.save()
            mixer.cycle(5).blend(resumes_models.Job, user=employee,
                                 city=random.choice([moscow, st_peter, chelyabinsk]))
            resume = mixer.blend(resumes_models.Resume, user=employee, photo='')
        else:
            employee = User.objects.get(username='employee')
        mixer.blend(recruiting_models.Response, vacancy__employer=employer, resume__user=employee)

    @staticmethod
    def create_employers():
        for _ in range(random.randint(10, 20)):
            user = mixer.blend(User, status=UserStatusChoices.EMPLOYER)
            Employer.objects.get(user=user).delete()
            mixer.blend(Employer, user=user, name=mixer.RANDOM, description=mixer.RANDOM,
                        phone=get_random_phone(), country=russia,
                        city=random.choice([moscow, st_peter, chelyabinsk]))

    @staticmethod
    def create_jobseekers():
        for _ in range(random.randint(10, 20)):
            user = mixer.blend(User, status=UserStatusChoices.JOBSEEKER)
            JobSeeker.objects.get(user=user).delete()
            mixer.blend(JobSeeker, user=user, date_birth=mixer.RANDOM,
                        sex=random.choice([SexChoices.MAN, SexChoices.WOMAN]),
                        phone=get_random_phone(), country=russia,
                        city=random.choice([moscow, st_peter, chelyabinsk]))

    @staticmethod
    def create_jobs():
        for _ in range(random.randint(10, 100)):
            mixer.blend(resumes_models.Job, user=mixer.SELECT,
                        user__status=UserStatusChoices.JOBSEEKER,
                        city=mixer.SELECT)

    @staticmethod
    def create_resumes():
        for _ in range(random.randint(10, 100)):
            resume = mixer.blend(resumes_models.Resume, user=mixer.SELECT,
                                 user__status=UserStatusChoices.JOBSEEKER)
            user_jobs = resumes_models.Job.objects.filter(user=resume.user)
            user_jobs = [j for j in user_jobs]
            for i in range(random.randint(0, len(user_jobs))):
                resume.jobs.add(user_jobs[i])
            resume.save()

    @staticmethod
    def create_vacancies():
        for _ in range(random.randint(10, 100)):
            mixer.blend(vacancies_models.Vacancy, employer=mixer.SELECT,
                        employer__status=UserStatusChoices.EMPLOYER, description=mixer.RANDOM,
                        hashtags=mixer.RANDOM, status=PublicStatusChoices.PUBLISHED)

    @staticmethod
    def create_blog():
        for _ in range(random.randint(10, 100)):
            mixer.blend(blog_models.Article)

    @staticmethod
    def create_responses():
        for _ in range(random.randint(10, 100)):
            response = mixer.blend(recruiting_models.Response, vacancy=mixer.SELECT, resume=mixer.SELECT,
                                   vacancy__status=PublicStatusChoices.PUBLISHED)
            responses = recruiting_models.Response.objects.filter(vacancy=response.vacancy,
                                                                  resume__user=response.resume.user)
            if len([resp for resp in responses]) > 1:
                response.delete()

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

    def import_fixtures(self):
        with open('conf/fixtures/companies.json', 'r', encoding='utf-8') as f:
            self.employers_fixtures = json.load(f, strict=False)
        with open('conf/fixtures/vacancies.json', 'r', encoding='utf-8') as f:
            self.vacancies_fixtures = json.load(f, strict=False)
        with open('conf/fixtures/news.json', 'r', encoding='utf-8') as f:
            self.news_fixtures = json.load(f, strict=False)

    def add_employers_from_fixtures(self):
        for employer_data in self.employers_fixtures:
            if 'name' not in employer_data or 'description' not in employer_data:
                continue
            user = mixer.blend(User, status=UserStatusChoices.EMPLOYER)
            Employer.objects.get(user=user).delete()
            mixer.blend(Employer, user=user, name=employer_data['name'],
                        description=employer_data['description'],
                        phone=get_random_phone(), country=russia,
                        city=random.choice([moscow, st_peter, chelyabinsk]))
            if employer_data['avatar']:
                user.avatar = employer_data['avatar'][0]['path']
                user.save()

    def add_vacancies_from_fixtures(self):
        for vacancy_data in self.vacancies_fixtures:
            if Employer.objects.filter(name=vacancy_data['company']).exists() and 'position' in vacancy_data:
                employer = Employer.objects.get(name=vacancy_data['company'])
                salary = vacancy_data['salary'] if 'salary' in vacancy_data else {}
                if salary and salary['min']:
                    salary = f'от {salary["min"]}' \
                             f'{(" до " + str(salary["max"])) if salary["max"] else ""}' \
                             f'{(" " + str(salary["currency"])) if salary["currency"] else ""}'
                else:
                    salary = ''
                mixer.blend(vacancies_models.Vacancy,
                            employer=employer.user,
                            title=vacancy_data['position'],
                            description=vacancy_data['description'] if 'description' in vacancy_data else '',
                            hashtags=vacancy_data['hashtags'] if 'hashtags' in vacancy_data else '',
                            salary=salary,
                            address=vacancy_data['address'] if 'address' in vacancy_data else '',
                            status=PublicStatusChoices.PUBLISHED)

    def add_blog_from_fixtures(self):
        for news_data in self.news_fixtures:
            news = mixer.blend(blog_models.Article,
                               title=news_data['title'],
                               description=news_data['description'],
                               author=news_data['author'])
            news.image = news_data['photo']
            news.save()
        for _ in range(random.randint(10, 20)):
            mixer.blend(blog_models.Article)

    def add_arguments(self, parser):
        parser.add_argument(
            '-j',
            '--json',
            action='store_true',
            default=False,
            help='Fill database using fixtures'
        )
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

            self.create_jobseekers()
            self.create_jobs()
            self.create_resumes()

            self.create_employers()
            self.create_vacancies()

            self.create_responses()
            self.create_offers()

            self.create_blog()
        elif options.get('json'):
            self.import_fixtures()
            self.add_blog_from_fixtures()

            self.create_suser()

            # self.create_jobseekers()
            # self.create_jobs()
            # self.create_resumes()

            self.add_employers_from_fixtures()
            self.add_vacancies_from_fixtures()

            # self.create_responses()
            # self.create_offers()

            self.create_blog()
        elif options.get('clear'):
            self.clear_db()
