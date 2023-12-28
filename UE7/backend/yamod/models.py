from django.db import models


class Genre(models.Model):

    name = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=1024)


class Movie(models.Model):

    movie_title = models.CharField(max_length=1024)
    original_title = models.CharField(max_length=1024, null=True)
    released = models.DateField()
    black_and_white = models.BooleanField(default=False)
    runtime = models.IntegerField(default=90, help_text="in minutes")
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True)
    genres = models.ManyToManyField(Genre)

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


class Role(models.Model):

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role = models.ForeignKey(RoleType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('person', 'movie', 'role')


class TVShow(models.Model):

    title = models.CharField(max_length=512)
    released = models.IntegerField()

    def __str__(self):
        return self.title


class Season(models.Model):

    season_no = models.IntegerField()
    cast = models.ManyToManyField(Person)
    tv_show = models.ForeignKey(TVShow, on_delete=models.PROTECT)

    class Meta:
        unique_together = ("season_no", "tv_show")

    def __str__(self):
        return str(self.season_no)


class Episode(models.Model):

    title = models.CharField(max_length=512)
    season = models.ForeignKey(Season, on_delete=models.PROTECT)
    length = models.PositiveIntegerField()

    def __str__(self):
        return self.title
