# Generated by Django 4.1.3 on 2023-12-04 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yamod', '0008_country_movie_country'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='genre',
            new_name='genres',
        ),
    ]
