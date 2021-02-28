from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework import viewsets
from .models import UserProfile

from rest_framework.views import APIView
from rest_framework.response import Response




class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class HelloApiView(APIView):
    """Test API view"""
    def get(self, request, format=None):
        """Return a list of APIView features"""
        an_apiview = [
            'Uses HTTP moethods as function (get, post, patch, put, delete)',
            'Is similar to a triditional django view',
            'Gives you the most control over you application logic', 
            'is mapped manually to URLs'
        ]
        return Response({'message': 'hello', 'an_apiview': an_apiview})