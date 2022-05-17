from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from src.kudos.models import Kudo
from src.users.models import User, Organization


class KudosModelTest(TestCase):

    def setUp(self):
        Organization.objects.create(name='test organization')
        self.from_user = User.objects.create(
            username='testUser',
            last_updated=datetime.now(),
            kudos_counter=3,
            organization_id=1
        )
        self.to_user = User.objects.create(
            username='testUser2',
            last_updated=datetime.now(),
            kudos_counter=3,
            organization_id=1
        )

    def test_kudo_model(self):
        kudo = Kudo.objects.create(
            from_user=self.from_user,
            to_user=self.to_user,
            date=datetime.now(),
            message='Great Job mate!',
        )
        self.assertEqual(kudo.message, 'Great Job mate!')


class KudoViewTest(APITestCase):

    def setUp(self):
        Organization.objects.create(name='test organization')
        self.from_user = User.objects.create(
            username='testUser',
            last_updated=datetime.now(),
            kudos_counter=3,
            organization_id=1
        )
        self.to_user = User.objects.create(
            username='testUser2',
            last_updated=datetime.now(),
            kudos_counter=3,
            organization_id=1
        )

        Kudo.objects.create(
            from_user=self.from_user,
            to_user=self.to_user,
            date=datetime.now(),
            message='Great Job mate!',
        )
        Kudo.objects.create(
            from_user=self.from_user,
            to_user=self.to_user,
            date=datetime.now(),
            message='Great Job friend!',
        )
        Kudo.objects.create(
            from_user=self.to_user,
            to_user=self.from_user,
            date=datetime.now(),
            message='Great Job Pal!',
        )
        Token.objects.create(user=self.from_user)
        token = Token.objects.get(user__username='testUser')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_user_kudos_view(self):
        url = reverse('kudos-received')
        response = self.client.get(url)
        kudos = Kudo.objects.filter(to_user=self.from_user).count()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(kudos, len(response.data))

    def test_user_kudos_view_no_auth(self):
        client = APIClient()
        url = reverse('kudos-received')
        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_give_kudos_with_enough_kudos(self):
        url = reverse('give-kudos', kwargs={'user_id': 2})
        data = {
            "message": "kudos"
        }
        old_user_kudos = self.from_user.kudos_counter
        response = self.client.post(url, data, format='json')
        user = User.objects.get(username='testUser')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.kudos_counter, (old_user_kudos - 1))

    def test_give_kudos_with_not_enough_kudos(self):
        url = reverse('give-kudos', kwargs={'user_id': 2})
        data = {
            "message": "kudos"
        }
        user = User.objects.get(username='testUser')
        user.kudos_counter = 0
        user.save()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Not Enough Kudos left for this Week :(.')

    def test_give_kudos_with_not_enough_kudos_refresh(self):
        url = reverse('give-kudos', kwargs={'user_id': 2})
        data = {
            "message": "kudos"
        }
        user = User.objects.get(username='testUser')
        user.kudos_counter = 0
        user.last_updated = datetime.now() - timedelta(days=10)
        user.save()
        response = self.client.post(url, data, format='json')

        # Get user after call to aPI
        user = User.objects.get(username='testUser')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.kudos_counter, 2)

    def test_give_kudos_to_self(self):
        url = reverse('give-kudos', kwargs={'user_id': 1})
        data = {
            "message": "kudos"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "Can't give your self kudos mate! :C")

