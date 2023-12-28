import json
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, User
from django.views import View
from django.shortcuts import render
from django.http import Http404

from django.core import serializers
from django.http import HttpResponse
from rest_framework.response import Response

from . import models
from .serializers import MovieSerializer


def serialize_model(self, serialized_entities):
    entities = []
    for entity in serialized_entities:
        entities.append(dict(pk=entity['pk'], name=entity['fields']['name']))
    return entities

class GenreView(View):

    def get(self, request):
        '''
        Task 1: Edit the genre view
        in a way that a request parameter
        order_by is accepted. The name of
        the parameter should be "order_by"
        and it accepts following input:

        order_by = -name  order by name in descending order
        order_by = name   order by name in ascending order

        if the parameter is not given at all, order by name
        in ascending order is assumed.

        Any values apart from 'name' should result in an
        error HTTP 400 (Bad request)
        '''
        # Your code starts here
        order_by = request.GET.get("order_by")
        if order_by in ["name", "-name"]:
            order_by_field = order_by
        elif order_by is None:
            order_by_field = "name"
        else:
            return HttpResponse(status=400)
        # Your code ends here
        genres = []
        for genre in models.Genre.objects.all().order_by(order_by_field):
            genres.append(genre.name)
        # Note: the .join string method takes a
        # list as input and concatenates the elements
        # by the character given in the string, thus
        # ",".join(["a","b","c"]) becomes "a,b,c"
        # "/".join(["a","b","c"]) becomes "a/b/c"
        return HttpResponse(",".join(genres))

class GenreAPIViewSet(viewsets.ViewSet):
    '''
    Simple API for Genre model
    '''

    def list(self, request):
        genres = []
        for genre in models.Genre.objects.all():
            genres.append({"id": genre.pk, "name": genre.name})
        return Response(genres)

    def create(self, request):
        if not(request.user.is_authenticated):
            return HttpResponse(status=401)
        payload = request.data
        if not("name" in payload):
            raise ValidationError("Property 'name' not found")
        models.Genre.objects.create(name=payload["name"])
        return Response(payload, status=201)

    def update(self, request, genre_pk):
        if not(request.user.is_authenticated):
            return HttpResponse(status=401)        
        payload = request.data
        genre = get_object_or_404(models.Genre, pk=genre_pk)
        if not("name" in payload):
            raise ValidationError("Property 'name' not found")
        models.Genre.objects.filter(pk=genre_pk).update(name=payload["name"])
        return Response(payload, status=200)

    def retrieve(self, request, genre_pk):
        genre = get_object_or_404(models.Genre, pk=genre_pk)
        return Response({"name": genre.name}, status=200)

    def destroy(self, request, genre_pk):
        if not(request.user.is_authenticated):
            return HttpResponse(status=401)        
        payload = request.data
        if request.user.groups.filter(name="Administrators").count() == 0:
            return Response({"error": "You need group 'Administrator'"}, status=403)
        genre = get_object_or_404(models.Genre, pk=genre_pk)
        models.Genre.objects.filter(pk=genre_pk).delete()
        return Response(payload, status=204)

class EpisodeAPIViewSet(viewsets.ViewSet):

    '''
    Simple API for Episode model
    '''

    def list(self, request):
        raise NotImplementedError()

    def create(self, request):
        raise NotImplementedError()

    def update(self, request, episode_pk):
        raise NotImplementedError()

    def retrieve(self, request, episode_pk):
        raise NotImplementedError()

    def destroy(self, request, episode_pk):
        raise NotImplementedError()

class EpisodeView(View):
    '''
    Task 2:
    Similar to the genre view, write a view that
    returns a list of Episodes in the databases
    following this format:

    "Name of Episode, Name of Episode"

    This time we want to have following
    query parameters (qp):

    (a) qp 'order_by': similar to the genre example; either accepts "length" or "title"
    if not given, the default order is title ascending
    (b) qp 'tv_show': allows to filter by the name of tv show the episode list should be
    generated for. Filtering should be done using a startswith query. If the qp is not
    given an error (HTTP 400) is raised.
    '''

    def get(self, request):
        tv_show = request.GET.get("tv_show")
        if tv_show is not None:
            query = models.Episode.objects.filter(season__tv_show__title__istartswith=tv_show)
        else:
            return HttpResponse(status=400)
        order_by = request.GET.get("order_by","title")
        if order_by in ["-title", "title", "length", "-length"]:
            order_by_clause = order_by
        else:
            return HttpResponse(status=400)
        # .values_list("title",flat=True) will transform the output into a list of strings, thus
        # ['Action','Comedy','Horror']
        # Finally, applying ",".join(["Action","Comedy","Horror"]) will produce the desired output 
        # format "Action,Comedy,Horror"
        return HttpResponse(",".join(query.order_by(order_by_clause).values_list("title", flat=True)))


class UserView(View):
    '''
    Task 3: Write a view that returns all users
    in the database. You have to be logged in to see the users.
    If users are assigned to a given group, they only see
    the users in this group
    '''

    def get(self, request):
        if not(request.user.is_authenticated):
            return HttpResponse(status=401)
        if request.user.is_superuser:
            users = get_user_model().objects.all().values_list("username", flat=True)
        # can be optimized:
        if request.user.groups.all():
            users = get_user_model().objects.filter(groups__in=request.user.groups.all()).values_list("username", flat=True)
        return HttpResponse(",".join(users))


class MovieView(View):

    def get(self, request):
        '''
        Task 1: Edit the genre view
        in a way that a request parameter
        order_by is accepted. The name of
        the parameter should be "order_by"
        and it accepts following input:

        order_by = -name  order by name in descending order
        order_by = name   order by name in ascending order

        if the parameter is not given at all, order by name
        in ascending order is assumed.

        Any values apart from 'name' should result in an
        error HTTP 400 (Bad request)
        '''
        # Your code starts here
        order_by = request.GET.get("order_by")
        if order_by in ["movie_title", "-movie_title"]:
            order_by_field = order_by
        elif order_by is None:
            order_by_field = "movie_title"
        else:
            return HttpResponse(status=400)
        # Your code ends here
        movies = []
        for movie in models.Movie.objects.all().order_by(order_by_field):
            movies.append(movie.movie_title)
        # Note: the .join string method takes a
        # list as input and concatenates the elements
        # by the character given in the string, thus
        # ",".join(["a","b","c"]) becomes "a,b,c"
        # "/".join(["a","b","c"]) becomes "a/b/c"
        return HttpResponse(",".join(movies))

class MovieAPIViewSet(viewsets.ViewSet):

    def serialize_model(self, serialized_entities):
        entities = []
        for entity in serialized_entities:
            entities.append(dict(pk=entity['pk'], name=entity['fields']['name']))
        return entities

    def list(self, request):
        movies = []
        for movie in models.Movie.objects.all():
            serialized_genres = serializers.serialize("python", movie.genres.all())
            genres = self.serialize_model(serialized_genres)
            movies.append({"pk": movie.pk,
                           "movie_title": movie.movie_title,
                           "original_title": movie.original_title,
                           "released": movie.released,
                           "runtime": movie.runtime,
                           "genres": genres,
                           "black_and_white": movie.black_and_white})
        return Response(movies)

    def create(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=201
            )
        else:
            return Response(serializer.errors, status=400)

    def update(self, request, pk):
        try:
            movie = models.Movie.objects.get(
                pk=pk
            )
            serializer = MovieSerializer(movie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=201
                )
            else:
                return Response(serializer.errors, status=400)
        except models.Movie.DoesNotExist:
            return Response(status=404)

    def retrieve(self, request, pk):
        movie = get_object_or_404(models.Movie, pk=pk)
        countries = None
        if movie.country is not None:
            serialized_countries = serializers.serialize('python', [movie.country], ensure_ascii=False,
                                                         fields=("id", "name"))
            countries = self.serialize_model(serialized_countries)

        serialized_genres = serializers.serialize("python", movie.genres.all())
        genres = self.serialize_model(serialized_genres)
        return Response({"pk": movie.pk,
                         "movie_title": movie.movie_title,
                         "released": movie.released,
                         "runtime": movie.runtime,
                         "black_and_white": movie.black_and_white,
                         "genres": genres,
                         "country": countries}, status=200)

    def destroy(self, request, pk):
        payload = request.data
        movie = get_object_or_404(models.Movie, pk=pk)
        models.Movie.objects.filter(pk=pk).delete()
        return Response(payload, status=204)
