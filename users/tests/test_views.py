from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class UserDetailViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
        test_user.save()
        
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('UserProfile'))
        self.assertRedirects(response, '/en-us/users/login/?next=/en-us/users/profile/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('UserProfile'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'users/user_detail.html')

class UserUpdateViewTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='1X<ISRUkw+tuK')
        test_user.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('UserUpdate'))
        self.assertRedirects(response, '/en-us/users/login/?next=/en-us/users/profile/update')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('UserUpdate'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'users/user_form.html')
    
    def test_update_user_correct(self):
        login = self.client.login(username='testuser', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse('UserUpdate'), {'username':'testupdateuser'})
        self.assertEqual(response.status_code, 200)
