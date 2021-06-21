# Generated by Django 3.2.3 on 2021-06-17 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicwork', '0004_rename_historic_historic_of_seeker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seeker',
            name='country',
            field=models.CharField(choices=[('BR', 'Brasil')], default='BR', max_length=2),
        ),
        migrations.AlterField(
            model_name='seeker',
            name='phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='phone'),
        ),
    ]