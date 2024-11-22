from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class AuthenticationTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password', email='test@example.com')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password'})
        self.assertRedirects(response, reverse('dashboard'))

    def test_logout(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
