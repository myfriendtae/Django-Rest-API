from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from api.models import Tag, Task, Business
from business import serializers


class BaseAttrViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    """ Base viewset for user owned  attributes """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Return objects for the current authenticated user only """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ create a new object """
        serializer.save(user=self.request.user)


class TagViewSet(BaseAttrViewSet):
    """ Manage tags in the database """
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
        
        
class TaskViewSet(BaseAttrViewSet):
    """ Manage tasks in the database """
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer


class BusinessViewSet(viewsets.ModelViewSet):
    """ Manage business in the database """
    queryset = Business.objects.all()
    serializer_class = serializers.BusinessSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Retrieve the objects for the authenticated user """
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """ Return serializer class"""
        if self.action == 'retrieve':
            return serializers.BusinessDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """ Create a new business """
        serializer.save(user=self.request.user)