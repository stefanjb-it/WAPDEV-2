# Generated by Django 4.1.3 on 2022-11-03 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yamod', '0004_episode'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='season',
            unique_together={('season_no', 'tv_show')},
        ),
    ]
