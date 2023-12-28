from django.contrib import admin
from . import models


class GenreAdmin(admin.ModelAdmin): pass

class TVShowAdmin(admin.ModelAdmin): pass
class SeasonAdmin(admin.ModelAdmin): pass
class PersonAdmin(admin.ModelAdmin): pass
class EpisodeAdmin(admin.ModelAdmin): pass
class MovieAdmin(admin.ModelAdmin): pass

admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Season, SeasonAdmin)
admin.site.register(models.Movie, MovieAdmin)
admin.site.register(models.Episode, EpisodeAdmin)
admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.TVShow, TVShowAdmin)

