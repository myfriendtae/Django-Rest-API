from rest_framework import serializers

from api.models import Tag, Task, Business

class TagSerializer(serializers.ModelSerializer):
    """ Serializer for tag objects """
    class Meta:
        model=Tag
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class TaskSerializer(serializers.ModelSerializer):
    """ Serializer for task objects """
    class Meta:
        model = Task
        fields = ('id', 'name')
        read_only_fields = ('id',)


class BusinessSerializer(serializers.ModelSerializer):
    """ Serializer for business objects"""
    tag = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    task = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Task.objects.all()
    )

    class Meta:
        model = Business
        fields = ('id', 'title', 'tag', 'task',)
        read_only_fields = ('id',)


class BusinessDetailSerializer(BusinessSerializer):
    """ Serializer for a business detail """
    tag = TagSerializer(many=True, read_only=True)
    task = TaskSerializer(many=True, read_only=True)


class BusinessImageSerializer(serializers.ModelSerializer):
    """ Serializer for uploading images to busines """
    class Meta:
        model = Business
        fields = ('id', 'image',)
        read_only_fields = ('id',)