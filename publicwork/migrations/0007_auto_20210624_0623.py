# Generated by Django 3.2.3 on 2021-06-24 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0002_alter_historic_description'),
        ('publicwork', '0006_publicworkgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicworkgroup',
            name='members',
            field=models.ManyToManyField(blank=True, to='publicwork.Seeker'),
        ),
        migrations.AlterField(
            model_name='publicworkgroup',
            name='mentors',
            field=models.ManyToManyField(blank=True, to='person.Person'),
        ),
    ]
