from rest_framework import serializers

from api.models import Tag, Task

class TagSerializer(serializers.ModelSerializer):
    """ Serializer for tag objects """
    class Meta:
        model=Tag
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class TaskSerializer(serializers.ModelSerializer):
    """ Serializer for task objexts """
    class Meta:
        model = Task
        fields = ('id', 'name')
        read_only_fields = ('id',)