from rest_framework import serializers
from django.contrib.auth.models import Group

class GroupSerializer(serializers.Serializer):

    name = serializers.CharField(required=True)

    def validate_name(self,data):
        if Group.objects.filter(name=data).exists():
            raise serializers.ValidationError("Group name already exists.")
        return data

    def create(self,validated_data):
        group = Group.objects.create(name=validated_data["name"])
        return group

    def update(self, instance, validated_data):        
        instance.name = validated_data.get("name")
        instance.save()
        return instance