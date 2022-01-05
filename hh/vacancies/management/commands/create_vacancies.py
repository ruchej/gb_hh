import random

from django.core.management import BaseCommand

from vacancies.models import Vacancy


class Command(BaseCommand):
    help = 'Create vacancies for testing'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='?', type=int, default=5)

    def handle(self, *args, **options):
        Vacancy.objects.all().delete()
        for i in range(options['count']):
            employment_type, _ = random.choice(Vacancy.EMPLOYMENT_TYPE_CHOICES)
            experience, _ = random.choice(Vacancy.EXPERIENCE_CHOICES)
            salary = round(random.randint(2, 14)) * 10000
            Vacancy.objects.create(
                employer=f'Vacancy №{i} employer',
                title=f'Vacancy №{i}',
                description=f'Vacancy №{i} description',
                experience=experience,
                employment_type=employment_type,
                salary=f'От {salary} р.'
            )
