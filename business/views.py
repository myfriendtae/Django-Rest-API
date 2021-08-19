from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
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

    def _params_to_ints(self, qs):
        """ Convert a list of string IDs to a list of intergers """
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """ Retrieve the objects for the authenticated user """
        tags = self.request.query_params.get('tag')
        tasks = self.request.query_params.get('task')
        queryset = self.queryset

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tag__id__in=tag_ids)
        if tasks:
            task_ids = self._params_to_ints(tasks)
            queryset = queryset.filter(task__id__in=task_ids)

        return queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """ Return serializer class"""
        if self.action == 'retrieve':
            return serializers.BusinessDetailSerializer
        elif self.action == 'upload_image':
            return serializers.BusinessImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """ Create a new business """
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ Upload an image to a busienss """
        business = self.get_object()
        serializer = self.get_serializer(
            business,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
