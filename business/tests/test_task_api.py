from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import serializers, status
from rest_framework.test import APIClient

from api.models import Task, Business
from business.serializers import TaskSerializer


TASK_URL = reverse('business:task-list')


class PublicTaskApiTest(TestCase):
    """ Test the publicly available task API """
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that login is required to access the endpoint """
        res = self.client.get(TASK_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTaskApiTests(TestCase):
    """ Test private tasks API """
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@email.com',
            'Password123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_task_list(self):
        """ Test retrieving a list of tasks """
        Task.objects.create(user=self.user, name="stock returns")
        Task.objects.create(user=self.user, name='account payable')

        res = self.client.get(TASK_URL)
        tasks = Task.objects.all().order_by('-name')
        serializer = TaskSerializer(tasks, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_task_limited_to_user(self):
        """ Test that tasks for the authenticated user are required """
        user2 = get_user_model().objects.create_user(
            'user2@email.com',
            'Password123'
        )
        Task.objects.create(user=user2, name='ingredient orders')
        task = Task.objects.create(user=self.user, name='account receivable')
        res = self.client.get(TASK_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], task.name)

    def test_create_task_successful(self):
        """ Test creating a new task """
        payload = { 'name' : 'payroll' }
        self.client.post(TASK_URL, payload)

        is_exist = Task.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(is_exist)

    def test_create_tag_invalid(self):
        """ Test creating a new tag with invalid payload """
        payload = { 'name': '' }
        res = self.client.post(TASK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tasks_assigned_to_business(self):
        """ Test filtering tasks by those assigned to busienss """
        task1 = Task.objects.create(user=self.user, name='finding a new customer')
        task2 = Task.objects.create(user=self.user, name='analysising a sales trend')
        business = Business.objects.create(
            title='sales',
            user=self.user
        )
        business.task.add(task1)
        res = self.client.get(TASK_URL, {'assigned_only': 1})

        serializer1 = TaskSerializer(task1)
        serializer2 = TaskSerializer(task2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_tasks_assiged_unique(self):
        """ Test filtering tasks by assigned to unique items """
        task1 = Task.objects.create(user=self.user, name='finding a new customer')
        task2 = Task.objects.create(user=self.user, name='analysising a sales trend')

        business1 = Business.objects.create(
            title='sales',
            user=self.user
        )
        business1.task.add(task1)

        business2 = Business.objects.create(
            title='order management',
            user=self.user
        )
        business2.task.add(task1)

        res = self.client.get(TASK_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)