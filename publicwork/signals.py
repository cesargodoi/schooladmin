from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Seeker, HistoricOfSeeker


@receiver(post_save, sender=Seeker)
def insert_historic(sender, instance, created, **kwargs):
    if created:
        date = timezone.now().date()
        instance.status = "MBR"
        instance.status_date = date
        instance.save()
        HistoricOfSeeker.objects.create(
            seeker=instance,
            occurrence="MBR",
            date=date,
            description="entered as a seeker",
            made_by=instance.made_by,
        )


@receiver(post_save, sender=HistoricOfSeeker)
def insert_status(sender, instance, created, **kwargs):
    if created:
        seeker = Seeker.objects.get(pk=instance.seeker.pk)
        seeker.status = instance.occurrence
        seeker.status_date = instance.date
        seeker.save()
