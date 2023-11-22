from django.contrib import admin

# Implement three model admin classes
# For each ModelAdmin, choose meaningful fields for list_display and list_filters attributes
# (1) PersonAdmin
# (2) MovieAdmin
# (3) RoleTypeAdmin
# (4) RoleAdmin

from django.contrib import admin
from . import models


class GenreAdmin(admin.ModelAdmin): pass


admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Series, GenreAdmin)
admin.site.register(models.Episode, GenreAdmin)
admin.site.register(models.Season, GenreAdmin)