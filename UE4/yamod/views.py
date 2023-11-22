from django.shortcuts import render

from django.contrib.auth.models import Group, User
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
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
        # Your code here (replace the HttpResponse too):
        html = ""
        if request.GET.get('order_by') is not None and request.GET.get('order_by') != '':
            for genre in models.Genre.objects.all().order_by(request.GET.get('order_by')):
                html = html + genre.name + "<br/>"
        else:
            for genre in models.Genre.objects.all().order_by('name'):
                html = html + genre.name + "<br/>"
        return HttpResponse(html)


class EpisodeView(View):
    '''
    Task 2:
    Similar to the genre view, write a view that
    returns a list of Episodes in the database
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
        # Your code here (replace the HttpResponse too):
        html = ""
        if request.GET.get('series') is not None and request.GET.get('series') != '':
            if (request.GET.get('order_by') == "runtime" or request.GET.get('order_by') == "-runtime" or
                    request.GET.get('order_by') == "episode_title" or request.GET.get('order_by') == "-episode_title"):
                res = models.Episode.objects.filter(
                    season__series__series_title__istartswith=request.GET.get('series')).order_by(
                    request.GET.get('order_by'))
            else:
                res = models.Episode.objects.filter(
                    season__series__series_title__istartswith=request.GET.get('series')).order_by('episode_title')
        else:
            return HttpResponse(status=400)
        for x in res:
            html = html + x.episode_title + ","
        return HttpResponse(html)


class UserView(View):
    '''
    Task 3: Write a view that returns all users
    in the database. You have to be logged in to see the users.

    - If you are not logged in, return a HTTP 401 error.
    - If you are logged in and you are a superuser you can see all users.
    - If you are logged in and you are assigned to a group, you can see all
    users assigned to that group.
    - If you are logged and you are not a superuser and you do not have
      any groups, you will not see any users.

    '''

    def get(self, request):
        # Your code here (replace the HttpResponse too):
        html = ""
        if request.user.is_authenticated:
            if request.user.is_superuser:
                for x in User.objects.all():
                    html = html + x.username + "<br/>"
            elif request.user.groups.all():
                for x in User.objects.filter(groups__in=request.user.groups.all()):
                    html = html + x.username + "<br/>"
            else:
                html="No GROUPS"

        else:
            return HttpResponse(status=401)


        return HttpResponse(html)
