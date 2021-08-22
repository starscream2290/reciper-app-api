from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user(email='cris@pldt.com', password='testpw'):
    "create a sample user"
    return get_user_model().objects.create_user(email,password)

class ModelTests(TestCase):
    def test_create_user_with_email_succ(self):
        "testing creating a new user with email"
        email='cayabyabcristopher@gmail.com'
        password='TestPass123'
        user=get_user_model().objects.create_user(
            email=email,
            password=password
            )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        "testing to normalized email for new user"
        email='cbcayabyab@PLDT.COM.PH'
        user=get_user_model().objects.create_user(email, "PW123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        "testing new user with no email"
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "PW123")

    def test_create_new_superuser(self):
        "testing a new superuser"
        user = get_user_model().objects.create_superuser(
            "superuser@pldt.com.ph",
            "pw123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        "Test the tag string representation"
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)
