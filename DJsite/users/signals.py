from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from services.services_models import create_new_profile_by_position


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        if hasattr(instance, '_position'):
            create_new_profile_by_position(instance)
