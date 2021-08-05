from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def set_up(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@gmail.com",
            password="admin123"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="normal@gmail.com",
            password="password123",
            name="normal user name"
        )
    
    # def test_user_page_change(self):
    #     """ Test that the user edit page works """
    #     url = reverse("admin:core_user_change", args=[self.id])
    #     res = self.client.get(url)
    #     self.assertEqual(res.status_code, 200)

    # def test_create_user_page(self):
    #     """ Test that the create user page works"""
    #     url = reverse("admin:core_user_add")
    #     res = self.client.get(url)
    #     self.assertEqual(res.status_code, 200)
