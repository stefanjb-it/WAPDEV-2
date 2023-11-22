# Generated by Django 4.1.3 on 2023-11-07 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yamod', '0006_revenue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='length',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=1024, unique=True),
        ),
        migrations.DeleteModel(
            name='Revenue',
        ),
    ]
