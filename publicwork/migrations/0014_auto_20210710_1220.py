# Generated by Django 3.2.5 on 2021-07-10 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicwork', '0013_alter_tempregofseeker_solicited_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seeker',
            name='image',
            field=models.ImageField(blank=True, default='default_profile.jpg', upload_to='seeker_pics'),
        ),
        migrations.AlterField(
            model_name='tempregofseeker',
            name='image',
            field=models.ImageField(blank=True, default='default_profile.jpg', upload_to='seeker_pics'),
        ),
    ]
