from django.conf import settings
from django.db import models
from schooladmin.common import (
    us_inter_char,
    short_name,
    GENDER_TYPES,
    LECTURE_TYPES,
    SEEKER_STATUS,
)


# Seeker
class Seeker(models.Model):
    center = models.ForeignKey(
        "center.Center",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=80)
    name_sa = models.CharField(max_length=80, editable=False)
    short_name = models.CharField(max_length=40, null=True, blank=True)
    birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_TYPES, default="M")
    image = models.ImageField(
        default="default_profile.jpg", upload_to="profile_pics"
    )
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField("state", max_length=2, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField("phone", max_length=15, blank=True)
    email = models.EmailField()
    status = models.CharField(max_length=3, choices=SEEKER_STATUS, blank=True)
    status_date = models.DateField(null=True, blank=True)
    observations = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="made_by_seeker",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.name_sa = us_inter_char(self.name)
        self.short_name = short_name(self.name)
        super(Seeker, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.name, self.center)

    class Meta:
        verbose_name = "seeker"
        verbose_name_plural = "seekers"


# Historic of seeker
class Historic(models.Model):
    seeker = models.ForeignKey(Seeker, on_delete=models.PROTECT)
    occurrence = models.CharField(
        max_length=3, choices=SEEKER_STATUS, default="NEW"
    )
    date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="made_by_historic_of_seeker",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"[{self.date}] {self.seeker.name} - {self.occurrence}"

    class Meta:
        verbose_name = "historic"
        verbose_name_plural = "historics"


# Lecture
class Lecture(models.Model):
    center = models.ForeignKey(
        "center.Center",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    type = models.CharField(max_length=3, choices=LECTURE_TYPES, default="CTT")
    theme = models.CharField(max_length=100)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    listeners = models.ManyToManyField(Seeker, through="Listener", blank=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    made_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_lecture",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.theme} [{self.type}] - {self.center} ({self.date})"

    class Meta:
        verbose_name = "lecture"
        verbose_name_plural = "lectures"
        ordering = ["date"]


#  Listener
class Listener(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.PROTECT)
    seeker = models.ForeignKey(Seeker, on_delete=models.PROTECT)
    ranking = models.IntegerField(default=0)
    observations = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.lecture} - {self.seeker} [{self.ranking}]"

    class Meta:
        verbose_name = "listener"
        verbose_name_plural = "listeners"
