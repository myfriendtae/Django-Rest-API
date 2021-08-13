from django.test import TestCase
from django.contrib.auth import get_user, get_user_model
from api.models import UserProfile, Tag, Task, Business


def sample_user(email='user@email.com', password='testpass'):
    """ Create a sample user """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """ Test creating a new user with an email is successful """
        email = 'user@email.com'
        password = 'Password123'
        user = get_user_model().objects.create_user(
            email=email,
            name='user name',
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Test the email for a new user is normalized """
        email = 'user@email.com'
        user = get_user_model().objects.create_user(email, 'Password123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test creating user with no email raises error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Password123')

    def test_create_new_super_user(self):
        """ Test creating super user """
        user = UserProfile.objects.create_superuser(
            'user@email.com',
            'Password123',
            'Password123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """ Test the tag string representation """
        tag = Tag.objects.create(
            user=sample_user(),
            name='Sales'
        )
        self.assertEqual(str(tag), tag.name)

    def test_task_str(self):
        """ Test the task string respresentation """
        task = Task.objects.create(
            user=sample_user(),
            name='stock returns'
        )
        self.assertEqual(str(task), task.name)

    def test_business_str(self):
        """ Test the business string representation """
        business = Business.objects.create(
            user=sample_user(),
            title='Butter'
        )
        self.assertEqual(str(business), business.title)