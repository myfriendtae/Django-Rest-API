from rest_framework import serializers
from django.contrib.auth import get_user, get_user_model
from api import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    class Meta:
        model = models.UserProfile
        fields = ('email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'},
                'min_length': 5
            }
        }

    def create(self, **validated_data):
        """Create and return a new user"""
        # user = models.UserProfile.objects.create_user(
        #     email=validated_data['email'],
        #     name=validated_data['name'],
        #     password=validated_data['password']
        # )
        user = models.UserProfile.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance
        return super().update(instance, validated_data)

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    '''Serializes profile feed items'''
    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {
            'user_profile':{
                'read_only': True
            }
        }

class MovieSerializer(serializers.ModelSerializer):
    """ Serialises movie items """
    class Meta:
        model = models.Movie
        fields = ('name', 'released_date', 'genre',)

class UserSerializer(serializers.ModelSerializer):
    """ Serialiser for the user object"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """ Create a new user with encrypted password and return it """
        return get_user_model().objects.create_user(**validated_data)
