from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from src.users.models import Organization, User


class UserModelTest(TestCase):

    def setUp(self):
        Organization.objects.create(name='test organization')
        User.objects.create(
            username='testUser',
            last_updated=datetime.now(),
            kudos_counter=3,
            organization_id=1
        )

    def test_user_model(self):
        user = User.objects.get(username='testUser')
        self.assertEqual(user.username, 'testUser')

    def test_organization_model(self):
        organization = Organization.objects.get(name='test organization')
        self.assertEqual(organization.name, 'test organization')


class UserViewTest(APITestCase):

    def setUp(self):
        Organization.objects.create(name='test organization')
        self.user = User.objects.create(
            username='testUser',
            last_updated=datetime.now(),
            kudos_counter=3,
            organization_id=1
        )
        User.objects.create(
            username='testUser2',
            last_updated=datetime.now(),
            kudos_counter=3,
            organization_id=1
        )
        Token.objects.create(user=self.user)
        token = Token.objects.get(user__username='testUser')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_user_detail_view(self):
        url = reverse('user-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testUser')

    def test_user_detail_view_no_auth(self):
        client = APIClient()
        url = reverse('user-profile')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_organization_detail_view(self):
        url = reverse('organization-list')
        response = self.client.get(url)
        organizations = User.objects.filter(organization__name=self.user.organization.name).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(organizations, len(response.data))

    def test_organization_detail_view_no_auth(self):
        client = APIClient()
        url = reverse('organization-list')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
