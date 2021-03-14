from django.shortcuts import render

from rest_framework import viewsets
from .models import UserProfile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from rest_framework.permissions import IsAuthenticated

from api import serializers
from api import models
from api import permissions


class HelloApiView(APIView):
    """Test API view"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Return a list of APIView features"""
        an_apiview = [
            'Uses HTTP moethods as function (get, post, patch, put, delete)',
            'Is similar to a triditional django view',
            'Gives you the most control over you application logic', 
            'is mapped manually to URLs'
        ]
        return Response({'message': 'hello', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a hellow message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})

# a simple CRUD interface to your database
# a quick and simple API
# no customisation on logic
class HelloViewSet(viewsets.ViewSet):
    '''Test API viewset'''

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        '''Return hello message'''
        a_viewset = [
            'use actions',
            'automatically map',
            'provide functionality'
        ]
        return Response({'message': 'hello from viewset', 'viewsets': a_viewset})

    
    def create(self, request):
        '''Create a new hello message'''
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        '''Handle getting an object by id'''
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        '''Handle updating an object'''
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        '''Handle updating part of an ojbect'''
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        '''Handle removing an object'''
        return Response({'http_method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    '''Handle creating and updating profiles'''
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email', )

class UserLoginApiView(ObtainAuthToken):
    '''Handle creating user authentication tokens'''
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    '''Handle creating, reading and updating profile feed items'''
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnSatus,
        IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        '''Sets the user profile to the logged in user'''
        serializer.save(user_profile=self.request.user)