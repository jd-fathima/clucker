"""Tests of the log in view """
from django.test import TestCase
from django.urls import reverse
from microblogs.forms import LogInForm
from microblogs.models import User
from .helpers import LogInTester

class LogInViewTestCase(TestCase, LogInTester):
    """Tests of the log in view """

    def setUp(self):
        self.url = reverse('log_in')
        User.objects.create_user('@johndoe',
        first_name='Jane',
        last_name='Doe',
        email= 'janedoe@example.org',
        bio ='Hello, I am John Doe',
        password='Password123'
    )

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/log_in/')


    def test_get_log_in(self):
        response = self.client.get(self.url)#getting login view
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)#display data entered again

    def test_unsuccessful_log_in(self):
        form_input = {'username': '@johndoe', 'password': 'WrongPassword123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)#display data entered again
        self.assertFalse(self._is_logged_in())

    def test_successful_log_in(self):
        form_input = {'username': '@johndoe', 'password': 'Password123'}#valid credential
        response = self.client.post(self.url, form_input, follow = True)#as we want client to follow redirect all the way to follow
        self.assertTrue(self._is_logged_in())
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')