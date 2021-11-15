from django.core.management.base import BaseCommand

from students.models import Student


class Command(BaseCommand):
    help = "Student generator, created by Django-extensions"

    def add_arguments(self, parser):
        parser.add_argument('count', nargs='?', type=int, default=10)

    def handle(self, *args, **options):
        count = options.get('count')
        Student.generate_entity(count)
        last_added = map(str, Student.objects.all().order_by('-id')[:count][::-1])
        sep = '\n'
        return f'List of students that were added:\n' \
               f'{sep.join(str(num) + ". " + value for num, value in enumerate(last_added, 1))}'
