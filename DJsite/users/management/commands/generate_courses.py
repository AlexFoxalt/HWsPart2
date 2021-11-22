from django.core.management.base import BaseCommand

from services.services_models import create_courses_from_1st_to_5th


class Command(BaseCommand):
    help = "Generate Courses from 1 to 5"

    def handle(self, *args, **options):
        create_courses_from_1st_to_5th()
        return 'Courses created!'
