from django.core.management.base import BaseCommand
from faker import Faker
from students.models import Student


fake = Faker('EN')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('count', nargs='?', type=int, default=10)

    def handle(self, *args, **options):
        count = options.get('count')
        for num in range(count):
            StudName = fake.name()
            StudCity = fake.city()
            Student.objects.create(name=StudName, city=StudCity)
        last_added = map(str, Student.objects.all().order_by('-id')[:count][::-1])
        sep = '\n'
        return f'List of students that were added:\n' \
               f'{sep.join(str(num) + ". " + value for num, value in enumerate(last_added, 1))}'
