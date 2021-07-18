from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@pldt.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@pldt.com',
            password='pw1234',
            name='test userako'
        )

    def test_users_listed(self):
        "test that users are listed on the user page"
        url = reverse('admin:core_user_changelist')
        responce = self.client.get(url)

        self.assertContains(responce, self.user.name)
        self.assertContains(responce, self.user.email)

    def test_user_change_page(self):
        "test that the user edit page works"
        url = reverse('admin:core_user_change',args=[self.user.id])
        responce = self.client.get(url)

        self.assertEqual(responce.status_code, 200)

    def test_create_user_page(self):
        "test that the create user page works"
        url = reverse('admin:core_user_add')
        responce = self.client.get(url)

        self.assertEqual(responce.status_code, 200)    
