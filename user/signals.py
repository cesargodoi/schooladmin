from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Profile
from person.models import Person


@receiver(post_save, sender=User)
def create_profile_and_person(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Person.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.is_active != instance.person.is_active:
        instance.person.is_active = instance.is_active
        instance.person.save()
    instance.profile.save()
