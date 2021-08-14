from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from api.models import Business, Tag, Task
from business.serializers import BusinessSerializer, BusinessDetailSerializer

BUSINESS_URL = reverse('business:business-list')


def detail_url(business_id):
    """ Return business detail URL """
    return reverse('business:business-detail', args=[business_id])

def sample_tag(user, name='sales team'):
    """ Create and return a sample tag """
    return Tag.objects.create(user=user, name=name)

def sample_task(user, name='sending sales infor to the order management'):
    """ create and return a sample task """
    return Task.objects.create(user=user, name=name)

def sample_business(user, **params):
    """ Create and return a sample recipe """
    defaults = {
        'title': 'sales',
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

    def test_view_business_detail(self):
        """ Test viewing a business detail """
        business = sample_business(user=self.user)
        business.tag.add(sample_tag(user=self.user))
        business.task.add(sample_task(user=self.user))
        
        url = detail_url(business.id)
        res = self.client.get(url)

        serializer = BusinessDetailSerializer(business)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_business(self):
        """ Test creating business """
        payload = {
            'title': 'sales',
        }
        res = self.client.post(BUSINESS_URL, payload)
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        
        business = Business.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(business, key))

    def test_create_business_with_tags(self):
        """ Test creating a business with tags """
        tag1 = sample_tag(user=self.user, name='sales team')
        tag2 = sample_tag(user=self.user, name='order management team')
        payload = {
            'title': 'sales',
            'tag': [tag1.id, tag2.id]
        }
        res = self.client.post(BUSINESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        business = Business.objects.get(id=res.data['id'])
        tags = business.tag.all()

        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_business_with_task(self):
        """ Test creating a business with tasks """
        task1 = sample_task(user=self.user, name='finding new customers')
        task2 = sample_task(user=self.user, name='collecting feedback from customers')
        payload = {
            'title': 'sales',
            'task': [task1.id, task2.id]
        }
        res = self.client.post(BUSINESS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        business = Business.objects.get(id=res.data['id'])
        tasks = business.task.all()

        self.assertEqual(tasks.count(), 2)
        self.assertIn(task1, tasks)
        self.assertIn(task2, tasks)