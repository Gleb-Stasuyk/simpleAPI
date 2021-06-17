from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from users.models import Profile
from companys.models import Company


class AuthViewsTests(APITestCase):

    def setUp(self):
        self.username = 'Test_User'
        self.password = 'password'
        self.user = User.objects.create_user(username='Test_User', password='password')
        self.company = Company.objects.create(company_name='Компания_1', bio='biobibobibibobibo')
        self.token_url = reverse('token_obtain_pair')
        self.data = {
            'username': self.username,
            'password': self.password
        }

    def test_admin_role(self):

        # Create a profile
        profile = Profile.objects.create(user=self.user, company=self.company, role='admin')
        self.assertEqual(self.user.is_active, 1, 'Active User')

        # First post to get token
        response = self.client.post(self.token_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        token = response.data['access']

        # Next post/get's will require the token to connect
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(reverse('company-list'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

        response = self.client.get(reverse('company-detail', args=['1']), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

        response = self.client.get(reverse('company-my_company'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

        response = self.client.delete(reverse('company-detail', args=['1']), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.content)


    def test_user_role(self):
        # Create a profile
        profile = Profile.objects.create(user=self.user, company=self.company, role='user')
        self.assertEqual(self.user.is_active, 1, 'Active User')

        # First post to get token
        response = self.client.post(self.token_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        token = response.data['access']

        # Next post/get's will require the token to connect
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(reverse('company-list'), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

        response = self.client.get(reverse('company-detail', args=['1']), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

        response = self.client.delete(reverse('company-detail', args=['1']), data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.content)