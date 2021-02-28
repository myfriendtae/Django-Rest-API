from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework import viewsets
from .models import UserProfile

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer