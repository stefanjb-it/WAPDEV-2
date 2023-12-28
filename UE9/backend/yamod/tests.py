import json
import time
import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from django.test import TestCase, Client
from django.urls import reverse
from django.db.models import Q
from . import models


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
        # Setup database
        [models.Genre.objects.create(name=name) for name in self.genres]
        [models.RoleType.objects.create(name=name) for name in ["Actor", "Producer", "Director"]]
        [models.Movie.objects.create(movie_title=movie_title,
                                     released=released,
                                     original_title=movie_title,
                                     runtime=runtime) for movie_title, released, genre, runtime in self.movies]
        # Updates
        for movie_title, released, genre, runtime in self.movies:
            models.Movie.objects.get(movie_title=movie_title).genre.add(models.Genre.objects.get(name=genre))


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
        movies_with_b_after_1980 = models.Movie.objects.filter(movie_title__startswith="B", released__year__gt=1980)
        # /ENDYOURCODE
        self.assertEqual(movies_with_b_after_1980.count(), 2)

    def test_or_query(self):
        # Filter all movies that were released after 2020 OR have genre comedy
        # YOUR CODE HERE:
        movies = models.Movie.objects.filter(Q(released__year__gt=2020) | Q(genre__name="Comedy"))
        # /ENDYOURCODE
        self.assertEqual(movies.count(), 2)

    def test_filter_relation(self):
        # Filter all movies where the genre ends with character "y"
        # YOUR CODE HERE:
        movies = models.Movie.objects.filter(genre__name__endswith="y")
        self.assertEquals(movies.count(), 2)
        # /ENDYOURCODE
        # Reverse relation
        # list all genre referenced by movies where the title starts with B:
        results = models.Genre.objects.filter(movie__movie_title__startswith="B")
        # if we want to get distinct results we use
        results = models.Genre.objects.filter(movie__movie_title__startswith="B").distinct()
        # this will not work in sqlite3, as sqlite3 does not support distinct on columns
        # (but this e.g. will work in postgresql)
        results = models.Genre.objects.filter(movie__movie_title__startswith="B").distinct("name")


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
        tv_show = models.TVShow.objects.create(title="Severance", released=2022)
        self.assertEquals(tv_show.released, 2022)

    def test_tv_show_season(self):
        '''
        Go to models.py and create a new model "Season".
        Write appropriate tests that show case how a new
        model instance is created and (optionally) updated and deleted.
        '''
        severance = models.TVShow.objects.create(title="Severance", released=2022)
        season = models.Season.objects.create(season_no=1, tv_show=severance)
        adam_scott = models.Person.objects.create(credited_name="Adam Scott", year_of_birth=1973, gender="m")
        season.cast.add(adam_scott)
        self.assertEquals(season.cast.count(), 1)
        # models.Season.objects.create(season_no=1,tv_show=severance)

    def test_tv_show_episode(self):
        '''
        Go to models.py and create a new model "Episode".
        Write appropriate tests that show case how a new
        model instance is created and (optionally) updated and deleted.
        '''
        severance = models.TVShow.objects.create(title="Severance", released=2022)
        season = models.Season.objects.create(season_no=1, tv_show=severance)
        adam_scott = models.Person.objects.create(credited_name="Adam Scott", year_of_birth=1973, gender="m")
        season.cast.add(adam_scott)
        episode = models.Episode.objects.create(title="Good News About Hell", season=season, length=50)
        self.assertEquals(episode.title, "Good News About Hell")


class GenreViewTests(YamodBaseTest):

    def test_genre_view(self):
        client = Client()
        url = reverse('genres')
        response = client.get(url)
        content = response.content.decode("utf-8")
        self.assertEqual(content, "Action,Comedy,Drama,Horror,Scifi")
        self.assertEqual(response.status_code, 200)

    def test_genre_view_asc(self):
        client = Client()
        url = reverse('genres')
        response = client.get(url+"?order_by=name")
        content = response.content.decode("utf-8")
        self.assertEqual(content, "Action,Comedy,Drama,Horror,Scifi")
        self.assertEqual(response.status_code, 200)

    def test_genre_view_desc(self):
        client = Client()
        url = reverse('genres')
        response = client.get(url+"?order_by=-name")
        content = response.content.decode("utf-8")
        self.assertEqual(content, "Scifi,Horror,Drama,Comedy,Action")
        self.assertEqual(response.status_code, 200)

    def test_genre_view_illegal_parameter(self):
        client = Client()
        url = reverse('genres')
        response = client.get(url+"?order_by=_Na_mee")
        self.assertEqual(response.status_code, 400)

class APIEpisodeViewTests(YamodBaseTest):

    def setUp(self):
        editors = Group.objects.create(name="Editors")
        self.member = get_user_model().objects.create_user(username="member",password="12345")
        self.member.groups.add(editors)
        self.admin  = get_user_model().objects.create_user(username="admin",password="12345",is_superuser=True)
        self.tv_show = models.TVShow.objects.create(title="My TV Show",released=1997)
        self.season = models.Season.objects.create(tv_show=self.tv_show,season_no=1)

    def get_token(self,admin=False):
        client = Client()
        client.login(username='member', password='12345')
        url = reverse("token_obtain_pair")
        # Your code here: make the request to the token_obtain_pair 
        # API endpoint providing username and password in this form:
        # {"username":"...", "password":"..."}
        # extract the "access" token from response and return it as string
        raise NotImplementedError()

    def test_create_not_authenticated(self):
        client = Client()
        # write a test to test if your interface returns 
        # 401 in case the user is not authenticated
        self.assertEqual(response.status_code, 401)

    def test_create(self):
        client = Client()
        token = self.get_token()
        url = reverse('episodes_api')
        # use this .post method call as template for the other methods:
        response = client.post(url, {"title":"Episode 1","season":1, "length":90}, 
                               HTTP_AUTHORIZATION="Bearer %s" % token,
                               content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_list(self):
        raise NotImplementedError()

    def test_update(self):
        raise NotImplementedError()

    def test_retrieve(self):
        raise NotImplementedError()
                

    def test_destroy(self):
        raise NotImplementedError()

class GenreRESTTests(YamodBaseTest):

    def setUp(self):
        get_user_model().objects.create_user(username="member1",password="12345")

    def test_genre_post(self):
        client = Client()
        client.login(username='member1', password='12345')
        url = reverse('genres_api')
        for genre in ["A","B","C"]:
            response = client.post(url, {"name":genre}, content_type='application/json')
            self.assertEqual(response.status_code, 201)        
        self.assertEqual(models.Genre.objects.filter(name="A").count(),1)
        self.assertEqual(models.Genre.objects.filter(name="B").count(),1)
        self.assertEqual(models.Genre.objects.filter(name="C").count(),1)
    
    def test_genre_post_malformed(self):
        client = Client()
        client.login(username='member1', password='12345')
        url = reverse('genres_api')        
        response = client.post(url, {}, content_type='application/json')
        self.assertEqual(response.status_code,400)

    def test_genre_post_name_none(self):
        client = Client()
        client.login(username='member1', password='12345')
        url = reverse('genres_api')        
        response = client.post(url, {"name":None}, content_type='application/json')
        self.assertEqual(response.status_code,400)

    def test_genre_post_already_exists(self):
        client = Client()
        client.login(username='member1', password='12345')
        url = reverse('genres_api')        
        response = client.post(url, {"name":"Action"}, content_type='application/json')        
        self.assertEqual(response.status_code,201)
        response = client.post(url, {"name":"Action"}, content_type='application/json')        
        self.assertEqual(response.status_code,409)        

class UserViewTests(YamodBaseTest):

    def setUp(self):
        user1 = get_user_model().objects.create(username="member1", is_superuser=True, is_active=True)
        user1.set_password("12345")
        user1.save()
        user2 = get_user_model().objects.create(username="member2", is_staff=False, is_active=True)
        user2.set_password("12345")
        user2.save()
        editors = Group.objects.create(name="editors")
        user2.groups.add(editors)

    def test_non_auth(self):
        client = Client()
        url = reverse('users')
        response = client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_superuser(self):
        client = Client()
        client.login(username='member1', password='12345')
        url = reverse('users')
        response = client.get(url)
        self.assertEqual(response.content.decode("utf-8"), "member1,member2")
        self.assertEqual(response.status_code, 200)

    def test_member(self):
        client = Client()
        client.login(username='member2', password='12345')
        url = reverse('users')
        response = client.get(url)
        self.assertEqual(response.content.decode("utf-8"), "member2")
        self.assertEqual(response.status_code, 200)


class EpisodeViewTests(YamodBaseTest):

    def setUp(self):
        star_trek = models.TVShow.objects.create(title="Star Trek TNG", released=1989)
        season_1 = models.Season.objects.create(season_no=1, tv_show=star_trek)
        models.Episode.objects.create(title="Far point station", length=48, season=season_1)
        models.Episode.objects.create(title="Code of Honor", length=47, season=season_1)

    def test_default_view(self):
        client = Client()
        url = reverse('episodes')
        response = client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_view_order_by_title_desc(self):
        client = Client()
        url = reverse('episodes')
        response = client.get(url+"?order_by=-title&tv_show=Star")
        self.assertEqual(response.content.decode("utf-8"), "Far point station,Code of Honor")

    def test_view_order_by_title_asc(self):
        client = Client()
        url = reverse('episodes')
        response = client.get(url+"?order_by=title&tv_show=Star")
        self.assertEqual(response.content.decode("utf-8"), "Code of Honor,Far point station")

    def test_view_order_by_length_desc(self):
        client = Client()
        url = reverse('episodes')
        response = client.get(url+"?order_by=-length&tv_show=Star")
        self.assertEqual(response.content.decode("utf-8"), "Far point station,Code of Honor")

    def test_view_order_by_length_asc(self):
        client = Client()
        url = reverse('episodes')
        response = client.get(url+"?order_by=length&tv_show=Star")
        # (Code of honor 47, Far point station 48)
        self.assertEqual(response.content.decode("utf-8"), "Code of Honor,Far point station")

    def test_view_search_tv_show(self):
        client = Client()
        for search_param in ["Star", "star"]:
            url = reverse('episodes')+f"?tv_show={search_param}"
            response = client.get(url)
            self.assertEqual(response.content.decode("utf-8"), "Code of Honor,Far point station")
        url = reverse('episodes')+f"?tv_show={search_param}"
        response = client.get(url)
        self.assertEqual(response.content.decode("utf-8"), "Code of Honor,Far point station")
