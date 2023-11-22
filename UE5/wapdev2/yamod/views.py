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

from django.http import HttpResponse
from rest_framework.response import Response

from . import models


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
        if not (request.user.is_authenticated):
            return HttpResponse(status=401)
        payload = request.data
        if not("name" in payload) or (payload["name"] is None):
            # raise ValidationError("Property 'name' not found")
            return Response(status=400)
        try:
            models.Genre.objects.create(name=payload["name"])
        except:
            return Response(status=409)
        return Response(payload, status=201)

    def update(self, request, genre_pk):
        if not (request.user.is_authenticated):
            return HttpResponse(status=401)
        payload = request.data
        if not("name" in payload) and not(payload["name"] is None):
            # raise ValidationError("Property 'name' not found")
            return Response(status=400)
        genre = get_object_or_404(models.Genre, pk=genre_pk)
        try:
            models.Genre.objects.filter(pk=genre_pk).update(name=payload["name"])
        except:
            return Response(status=400)
        return Response(payload, status=200)

    def retrieve(self, request, genre_pk):
        genre = get_object_or_404(models.Genre, pk=genre_pk)
        return Response({"name": genre.name}, status=200)

    def destroy(self, request, genre_pk):
        if not (request.user.is_authenticated):
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
        if not (request.user.is_authenticated):
            return HttpResponse(status=401)
        episodes = []
        for episode in models.Episode.objects.all():
            episodes.append({"id": episode.pk, "name": episode.title})
        return Response(episodes)

    def create(self, request):
        if not (request.user.is_authenticated):
            return HttpResponse(status=401)
        if request.user.groups.filter(name="Editors"):
            payload = request.data
            if not ("title" in payload) or (payload["title"] is None) or\
                not ("season" in payload) or (payload["season"] is None) or\
                not ("length" in payload) or (payload["length"] is None):
                # raise ValidationError("Property 'name' not found")
                return Response(status=400)
            # try:
            models.Episode.objects.create(title=payload["title"], season=(models.Season.objects.get(pk=payload["season"])), length=payload["length"])
            # except:
            # return Response(status=400)
        else:
            return Response(status=403)
        return Response(status=201)

    def update(self, request, episode_pk):
        if not (request.user.is_authenticated):
            return HttpResponse(status=401)
        raise NotImplementedError()

    def retrieve(self, request, episode_pk):
        if not (request.user.is_authenticated):
            return HttpResponse(status=401)
        episode = get_object_or_404(models.Episode, pk=episode_pk)
        return Response({"title": episode.title, "length": episode.length, "Season": episode.season.season_no, "TVShow": episode.season.tv_show.title}, status=200)

    def destroy(self, request, episode_pk):
        if not (request.user.is_authenticated):
            return HttpResponse(status=401)
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
        order_by = request.GET.get("order_by", "title")
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
        if not (request.user.is_authenticated):
            return HttpResponse(status=401)
        if request.user.is_superuser:
            users = get_user_model().objects.all().values_list("username", flat=True)
        # can be optimized:
        if request.user.groups.all():
            users = get_user_model().objects.filter(groups__in=request.user.groups.all()).values_list("username",
                                                                                                      flat=True)
        return HttpResponse(",".join(users))
