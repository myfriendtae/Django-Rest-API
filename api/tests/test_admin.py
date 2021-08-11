from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def set_up(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='superuser@email.com',
            password='Password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@email.com',
            password='Password123',
            name='user name'
        )
