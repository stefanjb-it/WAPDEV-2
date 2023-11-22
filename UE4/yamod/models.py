from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name



class Movie(models.Model):
    movie_title = models.CharField(max_length=1024)
    original_title = models.CharField(max_length=1024, null=True)
    released = models.DateField()
    runtime = models.IntegerField(default=90, help_text="in minutes")
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.movie_title


class Person(models.Model):
    GENDER_CHOICES = (
        ('m', 'male'),
        ('f', 'female'),
        ('x', 'diverse'),
    )

    credited_name = models.CharField(max_length=1024)
    year_of_birth = models.IntegerField()
    year_of_death = models.IntegerField(null=True, blank=True)
    participates_in = models.ManyToManyField(Movie, through="Role")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)


class RoleType(models.Model):
    name = models.CharField(max_length=1024, unique=True)

    def __str__(self):
        return self.name


class Series(models.Model):
    series_title = models.CharField(max_length=1024)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.series_title


class Season(models.Model):
    season_title = models.CharField(max_length=1024)
    start = models.DateField()
    end = models.DateField(blank=True, null=True)
    order = models.IntegerField()
    series = models.ForeignKey(Series, on_delete=models.CASCADE)

    def __str__(self):
        return self.season_title + ", " + self.series.series_title


class Episode(models.Model):
    episode_title = models.CharField(max_length=1024)
    runtime = models.IntegerField(default=90, help_text="in minutes")
    released = models.DateField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return self.episode_title


class Role(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role = models.ForeignKey(RoleType, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('person', 'movie', 'series', 'role')
