import datetime

from django.test import TestCase
from . import models
from django.db.models import Q


class YamodBaseTest(TestCase):

    def setUp(self):
        self.genres = ["Action", "Horror", "Scifi", "Drama", "Comedy"]
        self.movies = [
            ("Blade Runner", datetime.date(year=1982, month=6, day=25), "Scifi", 100),
            ("Blade Runner 2049", datetime.date(year=2017, month=10, day=6), "Scifi", 150),
            ("Nomadland", datetime.date(year=2020, month=9, day=11), "Drama", 110),
            ("The French Dispatch", datetime.date(year=2021, month=7, day=12), "Comedy", 100),
            ("Rushmoore", datetime.date(year=1998, month=9, day=17), "Comedy", 95)
        ]
        self.episodes = [
            ("Encounter at Farpoint", 92, datetime.date(year=1987, month=9, day=26), "Season 1",
             "Star Trek: The Next Generation"),
            ("Caretaker", 91, datetime.date(year=1995, month=1, day=16), "Season 1", "Star Trek: Voyager"),
            ("Pilot", 22, datetime.date(year=2013, month=12, day=2), "Season 1", "Rick and Morty"),
            ("Space Pilot 3000", 23, datetime.date(year=1999, month=3, day=28), "Season 1", "Futurama"),
            ("The End's Beginning", 61, datetime.date(year=2019, month=12, day=20), "Season 1", "The Witcher"),
        ]
        self.season = [
            ("Season 1", datetime.date(year=1987, month=9, day=28), datetime.date(year=1988, month=5, day=16), 1,
             "Star Trek: The Next Generation"),
            ("Season 2", datetime.date(year=1988, month=11, day=21), datetime.date(year=1989, month=7, day=17), 2,
             "Star Trek: The Next Generation"),
            ("Season 1", datetime.date(year=1995, month=1, day=16), datetime.date(year=1995, month=5, day=20), 1,
             "Star Trek: Voyager"),
            ("Season 2", datetime.date(year=1995, month=8, day=28), datetime.date(year=1996, month=5, day=20), 2,
             "Star Trek: Voyager"),
            ("Season 1", datetime.date(year=2013, month=12, day=2), datetime.date(year=2014, month=4, day=14), 1,
             "Rick and Morty"),
            ("Season 1", datetime.date(year=1999, month=3, day=28), datetime.date(year=1999, month=11, day=14), 1,
             "Futurama"),
            ("Season 1", datetime.date(year=1997, month=8, day=13), datetime.date(year=1998, month=2, day=25), 1,
             "South Park"),
            ("Season 1", datetime.date(year=2019, month=12, day=20), None, 1, "The Witcher"),
            ("Season 1", datetime.date(year=2021, month=1, day=8), None, 1, "Lupin"),
            ("Season 1", datetime.date(year=2013, month=9, day=12), datetime.date(year=2013, month=10, day=17), 1,
             "Peaky Blinders"),
        ]
        self.series = [
            ("Star Trek: The Next Generation", datetime.date(year=1987, month=9, day=28),
             datetime.date(year=1994, month=5, day=23), "Scifi"),
            ("Star Trek: Voyager", datetime.date(year=1995, month=1, day=16), datetime.date(year=2001, month=5, day=23),
             "Scifi"),
            ("Rick and Morty", datetime.date(year=2013, month=12, day=2), None, "Comedy"),
            ("Futurama", datetime.date(year=1999, month=3, day=28), None, "Comedy"),
            ("South Park", datetime.date(year=1997, month=8, day=13), None, "Comedy"),
            ("The Witcher", datetime.date(year=2019, month=12, day=20), None, "Drama"),
            ("Lupin", datetime.date(year=2021, month=1, day=8), None, "Action"),
            ("Peaky Blinders", datetime.date(year=2013, month=9, day=12), datetime.date(year=2022, month=4, day=3),
             "Drama")
        ]
        # Setup database
        [models.Genre.objects.create(name=name) for name in self.genres]
        [models.RoleType.objects.create(name=name) for name in ["Actor", "Producer", "Director"]]
        [models.Movie.objects.create(movie_title=movie_title,
                                     released=released,
                                     original_title=movie_title,
                                     runtime=runtime) for movie_title, released, genre, runtime in self.movies]
        [models.Series.objects.create(series_title=series_title,
                                      start=start,
                                      end=end
                                      ) for series_title, start, end, genre in self.series]
        [models.Season.objects.create(season_title=season_title,
                                      start=start,
                                      end=end,
                                      order=order,
                                      series=models.Series.objects.filter(series_title__exact=series).get()
                                      ) for season_title, start, end, order, series in self.season]
        [models.Episode.objects.create(episode_title=episode_title,
                                       runtime=runtime,
                                       released=released,
                                       season=models.Season.objects.filter(season_title__exact=season,
                                                                           series__series_title__exact=series).get()
                                       ) for episode_title, runtime, released, season, series in self.episodes]
        # Updates
        for movie_title, released, genre, runtime in self.movies:
            models.Movie.objects.get(movie_title=movie_title).genre.add(models.Genre.objects.get(name=genre))
        for series_title, start, end, genre in self.series:
            models.Series.objects.get(series_title__exact=series_title).genre.add(models.Genre.objects.get(name=genre))


class YamodModelTest(YamodBaseTest):

    def test_create_genre(self):
        # Create a new model instance for model "Genre" with name "Comedy"
        # YOUR CODE HERE:
        genre = models.Genre.objects.create(name="Comedy")
        # /ENDYOURCODE
        self.assertEqual(genre.name, "Comedy")

    def test_delete_genre(self):
        # YOUR CODE HERE: Delete Genre instance with name "Action"
        models.Genre.objects.filter(name="Action").delete()
        # /ENDYOURCODE
        self.assertEqual(models.Genre.objects.count(), 4)

    def test_filter_movie_by_year(self):
        # Filter all movies, that were released after 2000 (store results of query in variable movies_2000)
        # YOUR CODE HERE:
        movies_2000 = models.Movie.objects.filter(released__year__gte=2000)
        # /ENDYOURCODE        
        self.assertEqual(movies_2000.count(), 3)

    def test_filter_movie_by_runtime(self):
        # Filter all movies with a runtime <= 100 (FIXED: runtime < 100)
        # YOUR CODE HERE:
        movies_90 = models.Movie.objects.filter(runtime__lte=100)
        # /ENDYOURCODE
        self.assertEqual(movies_90.count(), 3)

    def test_filter_movie_starting_with_b(self):
        # Filter all movies that start with letter B
        # YOUR CODE HERE:
        movies_with_b = models.Movie.objects.filter(movie_title__startswith="B")
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
        for movie_title, released, genre, runtime in self.movies:
            self.assertEqual(str(models.Movie.objects.get(movie_title=movie_title)), movie_title)

    def test_update_role_type(self):
        # Load the model instance "Actor" of model "RoleType"
        # and update the name of the RoleType to "Actor/Actress"
        # YOUR CODE HERE:
        actor = models.RoleType.objects.get(name="Actor")
        actor.name = "Actor/Actress"
        actor.save()
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


class ExtendedQueryTests(YamodBaseTest):

    def test_and_query(self):
        # Filter all movies where the name starts with a B
        # AND that were released after 1980
        # YOUR CODE HERE:
        movies_with_b_after_1980 = models.Movie.objects.filter(movie_title__startswith="B", released__year__gte=1980)
        # /ENDYOURCODE
        self.assertEqual(movies_with_b_after_1980.count(), 2)

    def test_or_query(self):
        # Filter all movies that were released after 2020 OR have genre comedy
        # YOUR CODE HERE:
        movies = models.Movie.objects.filter(Q(released__year__gte=2020) | Q(genre__name="comedy"))
        # /ENDYOURCODE
        self.assertEqual(movies.count(), 2)

    def test_filter_relation(self):
        # Filter all movies where the genre ends with character "y"
        # YOUR CODE HERE:
        results = models.Movie.objects.filter(genre__name__endswith="y")
        # /ENDYOURCODE
        self.assertEqual(results.count(), 2)


class MigrationTests(YamodBaseTest):
    '''
    The goal of these tests, is to practice the use of the migrations 
    concept of Django. 
    
    Extend the data model of models.py to include the concept of 
    TV shows. The data model should at least provide models for 

    - TV shows (should have at least a title and a release date)
    - Seasons (should provide the possibility to add a regular cast referencing the Person model)
    - Episodes (should have at least a title and a length in minutes)

    and appropriate relations between them. Develop iterativley, 
    thus extend the data model one by one (always running 
    migrations between them) and implement the following test. 

    You can add further relations (e.g. tv shows and seasons 
    might have a link to genres) as you see fit.

    Optional: add custom django admin classes for the newly generated 
    models TV shows, seasons and episodes.

    '''

    def test_tv_show(self):
        '''
        Go to models.py and create a new model "TVShow". 
        Write appropriate tests that show case how a new 
        model instance is created and (optionally) updated and deleted.
        '''
        pass

    def test_tv_show_season(self):
        '''
        Go to models.py and create a new model "Season".
        Write appropriate tests that show case how a new 
        model instance is created and (optionally) updated and deleted.        
        '''
        pass

    def test_tv_show_episode(self):
        '''
        Go to models.py and create a new model "Episode".
        Write appropriate tests that show case how a new 
        model instance is created and (optionally) updated and deleted.        
        '''
        pass
