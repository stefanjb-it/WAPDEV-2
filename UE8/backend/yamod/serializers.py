from rest_framework import serializers

from . import models


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    # name = serializers.StringRelatedField(source='person')
    # Return list of names ['..'] instead a list of objects {name: '...'}
    def to_representation(self, obj):
        return obj.person.credited_name

    def to_internal_value(self, data):
        role = {
            "person_id": data
        }
        return role

    class Meta:
        model = models.Role

        fields = ['person']


class Country:
    pass


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Movie
        fields = '__all__'

    def create(self, validated_data):
        genre_data = validated_data.pop('genres')
        movie = models.Movie.objects.create(**validated_data)
        for genre in genre_data:
            movie.genres.add(genre.pk)
        return movie

    def update(self, instance, validated_data):
        genre_data = validated_data.pop('genres')
        instance.movie_title = validated_data.get('movie_title', instance.movie_title)
        instance.runtime = validated_data.get('runtime', instance.runtime)
        instance.released = validated_data.get('released', instance.released)
        instance.save()

        instance.genres.clear()

        for genre in genre_data:
            print(genre)
            instance.genres.add(genre.pk)

        return instance
