from django.db.models.signals import post_save, pre_save, post_delete, pre_delete #noqa
from django.dispatch import receiver
from django.contrib.auth.models import User
from faunatrack.models import Scientifique

@receiver(post_save, sender=User)
def add_scientifique_when_user_created(sender, instance, created, **kwargs):
    if created:
        Scientifique.objects.create(user=instance)