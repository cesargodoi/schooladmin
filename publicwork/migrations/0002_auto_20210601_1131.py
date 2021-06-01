# Generated by Django 3.2.3 on 2021-06-01 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicwork', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seeker',
            name='status',
            field=models.CharField(blank=True, choices=[('NEW', 'new'), ('MT1', 'meeting 1'), ('MT2', 'meeting 2'), ('DNL', 'did not like'), ('REG', 'regular'), ('SVC', 'service'), ('CNF', 'conference'), ('INS', 'installing'), ('TKG', 'thinking'), ('RST', 'restriction')], max_length=3),
        ),
        migrations.AddField(
            model_name='seeker',
            name='status_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historic',
            name='occurrence',
            field=models.CharField(choices=[('NEW', 'new'), ('MT1', 'meeting 1'), ('MT2', 'meeting 2'), ('DNL', 'did not like'), ('REG', 'regular'), ('SVC', 'service'), ('CNF', 'conference'), ('INS', 'installing'), ('TKG', 'thinking'), ('RST', 'restriction')], default='NEW', max_length=3),
        ),
    ]
