import django
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from services.services_constants import FAKER
from services.services_functions import mine_faker_of_faculties


def create_random_user(position):
    first_name = FAKER.first_name()
    last_name = FAKER.last_name()
    nickname = f'bot_{first_name.lower()}_{last_name.lower()}'

    user = get_user_model()(
        email=FAKER.email(),
        nickname=nickname,
        first_name=first_name,
        last_name=last_name
    )
    user.set_password('123faker123')
    # Set some extra attrs to the instance to be used in the handler.
    user._position = position

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
