# Generated by Django 3.2.3 on 2021-05-19 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Center",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                (
                    "short_name",
                    models.CharField(blank=True, max_length=25, null=True),
                ),
                ("address", models.CharField(blank=True, max_length=50)),
                ("number", models.CharField(blank=True, max_length=10)),
                ("complement", models.CharField(blank=True, max_length=50)),
                ("district", models.CharField(blank=True, max_length=50)),
                ("city", models.CharField(blank=True, max_length=50)),
                (
                    "state",
                    models.CharField(
                        blank=True, max_length=2, verbose_name="state"
                    ),
                ),
                (
                    "country",
                    models.CharField(
                        choices=[("BR", "Brasil")], default="BR", max_length=2
                    ),
                ),
                (
                    "zip_code",
                    models.CharField(
                        blank=True, max_length=15, verbose_name="zip code"
                    ),
                ),
                (
                    "phone_1",
                    models.CharField(
                        blank=True, max_length=15, verbose_name="phone"
                    ),
                ),
                (
                    "phone_2",
                    models.CharField(
                        blank=True, max_length=15, verbose_name="backup phone"
                    ),
                ),
                ("email", models.CharField(blank=True, max_length=60)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default="default_center.jpg",
                        upload_to="center_pics",
                    ),
                ),
                (
                    "pix_image",
                    models.ImageField(
                        blank=True,
                        default="default_center.jpg",
                        upload_to="center_pix_pics",
                    ),
                ),
                (
                    "pix_key",
                    models.CharField(
                        blank=True, max_length=50, null=True, unique=True
                    ),
                ),
                (
                    "center_type",
                    models.CharField(
                        choices=[
                            ("CNT", "center"),
                            ("CNF", "conference center"),
                            ("CTT", "contact room"),
                        ],
                        default="CNT",
                        max_length=3,
                        verbose_name="type",
                    ),
                ),
                ("observations", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "conf_center",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="center.center",
                    ),
                ),
                (
                    "made_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="made_by_center",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "secretary",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="secretary",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "center",
                "verbose_name_plural": "centers",
                "ordering": ["name"],
            },
        ),
    ]
