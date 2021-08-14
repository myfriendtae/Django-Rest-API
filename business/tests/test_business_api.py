from django.contrib.auth import get_user_model
from django.test import TestCase, testcases
from django.urls import reverse

from rest_framework import serializers, status
from rest_framework.test import APIClient

from api.models import Business
from business.serializers import BusinessSerializer

BUSINESS_URL = reverse('business:business-list')

def sample_business(user, **params):
    """ Create and return a sample recipe """
    defaults = {
        'title': 'Butter',
    }
    defaults.update(params)
    return Business.objects.create(user=user, **defaults)


class PublicBusinessApiTests(TestCase):
    """ Test unauthenticated business API enpoint """
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test authentication is required """
        res = self.client.get(BUSINESS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBusinessApiTests(TestCase):
    """ Test untehnticated business API enpoint """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@emaail.com',
            'Password123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_business(self):
        """ Test retrieving a list of businesses """
        sample_business(user=self.user)
        sample_business(user=self.user)

        res = self.client.get(BUSINESS_URL)

        business = Business.objects.all().order_by('-id')
        serializer = BusinessSerializer(business, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_business_limited_to_user(self):
        """ Test retrieving business for user """
        user2 = get_user_model().objects.create_user(
            'user2@email.com',
            'Password123'
        )
        sample_business(user=user2)
        sample_business(user=self.user)
        
        res =self.client.get(BUSINESS_URL)

        business = Business.objects.filter(user=self.user)
        serializer = BusinessSerializer(business, many=True)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
