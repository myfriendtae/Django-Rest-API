from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from api.models import Tag, Business
from business import serializers
from business.serializers import TagSerializer


TAG_URL = reverse('business:tag-list')


class PublicTagApiTests(TestCase):
    """ Test the business api enpoint """
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test the login is required for retreiving tags """
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTests(TestCase):
    """ Test the business api enpoint """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@email.com',
            'Password123'
        )
        self.client.force_authenticate(self.user)

    def test_retreive_tags(self):
        """ Test retrieving tags """
        Tag.objects.create(user=self.user, name='Manufacturing')
        Tag.objects.create(user=self.user, name='Sales')

        res = self.client.get(TAG_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_owner(self):
        """ Test that tags returned are for the authenticated users """
        user2 = get_user_model().objects.create_user(
            'user2@email.com',
            'Password123'
        )
        Tag.objects.create(user=user2, name='Warehouse')
        tag = Tag.objects.create(user=self.user, name='Sales')
        res = self.client.get(TAG_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """ Test creating a new tag """
        payload = { 'name': 'test tag' }
        self.client.post(TAG_URL, payload) 

        is_exist = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        
        self.assertTrue(is_exist)

    def test_create_tag_invalid(self):
        """ Test creating a new tag with invalid payload """
        payload = { 'name': '' }
        res = self.client.post(TAG_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tags_assigned_to_business(self):
        """ Test filtering tags by those assigned to busienss """
        tag1 = Tag.objects.create(user=self.user, name='order management')
        tag2 = Tag.objects.create(user=self.user, name='sales')
        business = Business.objects.create(
            title='sales',
            user=self.user
        )
        business.tag.add(tag1)
        res = self.client.get(TAG_URL, {'assigned_only': 1})

        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_tags_assiged_unique(self):
        """ Test filtering tags by assigned to unique items """
        tag1 = Tag.objects.create(user=self.user, name='sales')
        tag2 = Tag.objects.create(user=self.user, name='order management')

        business1 = Business.objects.create(
            title='sales',
            user=self.user
        )
        business1.tag.add(tag1)

        business2 = Business.objects.create(
            title='order management',
            user=self.user
        )
        business2.tag.add(tag1)

        res = self.client.get(TAG_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)