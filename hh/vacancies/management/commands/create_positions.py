from django.core.management import BaseCommand

from vacancies.models import Position


class Command(BaseCommand):
    help = 'Create positions for testing'

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='?', type=int, default=5)

    def handle(self, *args, **options):
        Position.objects.all().delete()
        for position_title, _ in Position.POSITION_CHOICES:
            position = Position.objects.create(
                title=position_title
            )
