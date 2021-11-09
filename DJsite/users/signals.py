from django.db.models.signals import post_save
from django.dispatch import receiver

from services.services_models import create_new_profile_by_position
from users.models import CustomUser


@receiver(post_save, sender=CustomUser)
def update_profile_signal(sender, instance, created, **kwargs):
    if created and hasattr(instance, '_position'):
        create_new_profile_by_position(instance)
