"""wapdev2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from userapi import views as user_views
from yamod import views as yamod_views

urlpatterns = [
    # Django Admin URLs:
    path('admin/', admin.site.urls),
    # user and authentication apis:
    path('api/', user_views.ApiView.as_view({'get': "list"})),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', user_views.UserViewSet.as_view({"get": "list",
                                                       "post": "create"})),
    path('api/users/<pk>', user_views.UserViewSet.as_view({"get": "retrieve",
                                                           "put": "update",
                                                           "delete": "destroy", })),
    path('api/users/<user_pk>/security', user_views.SecurityViewSet.as_view({"put": "update", "get": "list"})),
    path('api/users/<user_pk>/image', user_views.ImageProfileViewSet.as_view({"get": "retrieve", "post": "create"})),
    path('api/users/<user_pk>/groups', user_views.UserGroupViewSet.as_view({"post": "create", "get": "list"})),
    path('api/users/<user_pk>/groups/<group_pk>', user_views.UserGroupViewSet.as_view({"delete": "destroy", "get": "retrieve"})),
    path('api/groups', user_views.GroupViewSet.as_view({'get': "list", "post": "create"})),
    path('api/groups/<group_pk>', user_views.GroupViewSet.as_view({'put': "update", "delete": "destroy", "get": "retrieve"})),
    # yamod urls
    path('genres/', yamod_views.GenreView.as_view(), name="genres"),
    path('episodes/', yamod_views.EpisodeView.as_view(), name="episodes"),
    path('users/', yamod_views.UserView.as_view(), name="users"),    
    # yamod api urls
    path('api/genres/', yamod_views.GenreAPIViewSet.as_view({"get": "list", "post" : "create"}), name="genres_api"),
    path('api/genres/<pk>', yamod_views.GenreAPIViewSet.as_view({'put': "update", "delete": "destroy", "get": "retrieve"}), name="genres_api"),
    path('api/episodes/', yamod_views.EpisodeAPIViewSet.as_view({"get": "list", "post": "create"}), name="episodes_api"),
    path('api/episodes/<pk>',
         yamod_views.EpisodeAPIViewSet.as_view({'put': "update", "delete": "destroy", "get": "retrieve"}),
         name="episodes_api"),
]

if settings.DEBUG:
    # Adding "static" to the urlpatterns makes all file uploads visible in the admin.
    # This is OK on development servers (hence, the settings.DEBUG check) but should never
    # be deployed to production environments as it exposes all uploads to the world.
    urpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
