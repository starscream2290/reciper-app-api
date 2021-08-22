from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer
#tag-serializers to make the test pass after we write the unit tests

TAGS_URL = reverse ('recipe:tag-list')
#url is tag-list, and will be using a view set that automatically appends the action name to the end of the url using the router
#tag-list: for listing tags

class PublicTagsApiTests(TestCase):
    "Test the publicly available tags API"

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        "Test that login is required for retrieving tags"
        responce = self.client.get(TAGS_URL) #makes an unauthenticated request to tags API url

        self.assertEqual(responce.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    "Test the authorized user tags API"

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@pldt.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        "Test retrieving tags"
        #setup by creating sample tags then request to the API and then check that a tag return equal that are expecte to be equal
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        responce = self.client.get(TAGS_URL)
        #makes an HTTP req to the url that should return the tags

        tags = Tag.objects.all().order_by('-name')  # tags are in alphabetical order in revers
        "make a query on the model that expect to get the compare the results"
        serializer = TagSerializer(tags, many=True) #multiple tags

        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(responce.data, serializer.data)
        #res.data is return on the responce and expected to be the same as serializer.data

    def test_tags_limited_to_user(self):
        "Test that tags returned are for the authenticated user"
        user2 = get_user_model().objects.create_user(
            'user2@pldt.com',
            'user2pw'
        )
        #new user assign a tag to that user and that is not included on the respone as not included on the authenticated user

        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')
        #new tags that assign to a authenticated user

        respone = self.client.get(TAGS_URL)
        #only one tag to be return as authenticated to the user

        self.assertEqual(respone.status_code, status.HTTP_200_OK)
        self.assertEqual(len(respone.data), 1)
        self.assertEqual(respone.data[0]['name'], tag.name)
