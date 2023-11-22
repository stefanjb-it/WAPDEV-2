import datetime

from django.test import TestCase
from . import models


class YamodModelTest(TestCase):

    def setUp(self):
        self.genres = ["Action", "Horror", "Scifi"]
        self.movies = [
            ("Blade Runner", datetime.date(year=1982, month=6, day=25), 100),
            ("Blade Runner 2049", datetime.date(year=2017, month=10, day=6), 150),
            ("Nomadland", datetime.date(year=2020, month=9, day=11), 110),
            ("The French Dispatch", datetime.date(year=2021, month=7, day=12), 100),
            ("Rushmoore", datetime.date(year=1998, month=9, day=17), 95)
        ]
        # Setup database
        [models.Genre.objects.create(name=name) for name in ["Action", "Horror", "Scifi"]]
        [models.RoleType.objects.create(name=name) for name in ["Actor", "Producer", "Director"]]
        [models.Movie.objects.create(movie_title=movie_title,
                                     released=released,
                                     original_title=movie_title,
                                     runtime=runtime) for movie_title, released, runtime in self.movies]

    def test_create_genre(self):
        # Create a new model instance for model "Genre" with name "Comedy" (model instance should be stored in variable 'genre')
        # YOUR CODE HERE:
        genre = models.Genre.objects.create(name="Comedy")
        # /ENDYOURCODE
        self.assertEqual(genre.name, "Comedy")

    def test_delete_genre(self):
        # YOUR CODE HERE: Delete Genre instance with name "Action"
        models.Genre.objects.filter(name__exact="Action").delete()
        # /ENDYOURCODE
        self.assertEqual(models.Genre.objects.count(), 2)

    def test_filter_movie_by_year(self):
        # Filter all movies, that were released after 2000 (store results of query in variable movies_2000)
        # YOUR CODE HERE:
        movies_2000 = models.Movie.objects.filter(released__gt="1999-12-31")
        # /ENDYOURCODE
        self.assertEqual(movies_2000.count(), 3)

    def test_filter_movie_by_runtime(self):
        # Filter all movies with a runtime <= 100
        # YOUR CODE HERE:
        movies_90 = models.Movie.objects.filter(runtime__lte=100)
        # /ENDYOURCODE
        self.assertEqual(movies_90.count(), 3)

    def test_filter_movie_starting_with_b(self):
        # Filter all movies that start with letter B
        # YOUR CODE HERE:
        movies_with_b = models.Movie.objects.filter(movie_title__istartswith="B")
        # /ENDYOURCODE
        self.assertEqual(movies_with_b.count(), 2)

    def test_filter_movie_containing_blade(self):
        # Filter all movies that contain "Blade" in its title
        # YOUR CODE HERE:
        movies_containing_blade = models.Movie.objects.filter(movie_title__contains="Blade")
        # /ENDYOURCODE
        self.assertEqual(movies_containing_blade.count(), 2)

    def test_genre_to_str(self):
        # Implement the __str__ method of model class Genre and Movie
        # Genre should return the name and Movie should return the movie_title
        # (Implementation is done in models.py)
        for movie_title, released, runtime in self.movies:
            self.assertEqual(str(models.Movie.objects.get(movie_title=movie_title)), movie_title)

    def test_update_role_type(self):
        # Load the model instance "Actor" of model "RoleType"
        # and update the name of the RoleType to "Actor/Actress"
        # YOUR CODE HERE:
        models.RoleType.objects.filter(name__exact="Actor").update(name="Actor/Actress")
        # /ENDYOURCODE
        self.assertEqual(models.RoleType.objects.filter(name="Actor/Actress").count(), 1)

    def test_get_or_create_role_type(self):
        # The following call results in an error, as a role type "Producer"
        # already exists. Modify the "create" method accordingly, so this
        # test can pass
        # MODIFY CODE HERE
        models.RoleType.objects.get_or_create(name="Producer")
        # /ENDYOURCODE
        self.assertEqual(models.RoleType.objects.count(), 3)
        self.assertEqual(models.RoleType.objects.filter(name="Producer").count(), 1)
