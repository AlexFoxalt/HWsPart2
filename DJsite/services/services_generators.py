import django
from django.contrib.auth.models import User, Group

from services.services_constants import FAKER
from services.services_functions import mine_faker_of_faculties


def create_random_user():
    first_name = FAKER.first_name()
    last_name = FAKER.last_name()

    user = User(
        username=f'gen_{first_name}_{last_name}',
        email=FAKER.email(),
        first_name=first_name,
        last_name=last_name
    )
    user.set_password('123faker123')
    user.save()

    try:
        my_group = Group.objects.get(name='Client')
    except django.contrib.auth.models.Group.DoesNotExist:
        client_group = Group.objects.create(name='Client')
        staff_group = Group.objects.create(name='Staff')
        my_group = client_group

    my_group.user_set.add(user)

    return user


def create_random_profile_data(user):
    profile_data = {
        'user': user,
        'city': FAKER.city(),
        'phone_number': FAKER.phone_number(),
        'faculty': mine_faker_of_faculties(),
        'filled': True
    }
    return profile_data
