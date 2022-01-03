import random

from django.core.management import BaseCommand

from vacancies.models import Vacancy, Position


class Command(BaseCommand):
    help = 'Create vacancies for testing'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='?', type=int, default=5)

    def handle(self, *args, **options):
        Vacancy.objects.all().delete()
        positions = Position.objects.all()
        for i in range(options['count']):
            position = random.choice(positions)
            employment_type, _ = random.choice(Vacancy.EMPLOYMENT_TYPE_CHOICES)
            vacancy = Vacancy.objects.create(
                employer=f'Vacancy №{i} employer',
                title=f'Vacancy №{i}',
                description=f'Vacancy №{i} description',
                employment_type=employment_type
            )
            vacancy.positions.add(position)
