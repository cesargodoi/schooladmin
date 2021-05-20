from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Seeker, Historic


@receiver(post_save, sender=Seeker)
def insert_historic(sender, instance, created, **kwargs):
    if created:
        Historic.objects.create(
            seeker=instance,
            occurrence="new",
            date=timezone.now().date(),
            description="entered as a seeker",
            made_by=instance.made_by,
        )
