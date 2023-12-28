# Generated by Django 4.1.3 on 2022-11-03 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_title', models.CharField(max_length=1024)),
                ('original_title', models.CharField(max_length=1024, null=True)),
                ('released', models.DateField()),
                ('runtime', models.IntegerField(default=90, help_text='in minutes')),
                ('genre', models.ManyToManyField(to='yamod.genre')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credited_name', models.CharField(max_length=1024)),
                ('year_of_birth', models.IntegerField()),
                ('year_of_death', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('m', 'male'), ('f', 'female'), ('x', 'diverse')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='RoleType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yamod.movie')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yamod.person')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yamod.roletype')),
            ],
            options={
                'unique_together': {('person', 'movie', 'role')},
            },
        ),
        migrations.AddField(
            model_name='person',
            name='participates_in',
            field=models.ManyToManyField(through='yamod.Role', to='yamod.movie'),
        ),
    ]
