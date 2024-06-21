import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, Message
from .forms import ProfileForm, UserRegistrationForm, MessageForm

class UserRegistrationTest(TestCase):
    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        })
        if response.status_code != 302:
            print(response.content)  # Вывод содержимого страницы для диагностики
        self.assertEqual(response.status_code, 302)  # Successful registration should redirect
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Profile.objects.filter(user__username='testuser').exists())  # Проверка создания профиля


class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password12345')

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password12345'
        })
        self.assertEqual(response.status_code, 302)  # Successful login redirects to home page
        self.assertTrue(response.wsgi_request.user.is_authenticated)

class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password12345')
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username='testuser', password='password12345')

    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_update(self):
        response = self.client.post(reverse('profile'), {
            'bio': 'Test Bio',
            'location': 'Test Location',
            'birth_date': '2000-01-01',
            'phone_number': '1234567890'
        })
        self.assertEqual(response.status_code, 302)  # Successful update redirects to profile page
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'Test Bio')

class MessageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password12345')
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username='testuser', password='password12345')
        self.message = Message.objects.create(sender=self.user, subject='Test Subject', message='Test Message')

    def test_message_list(self):
        response = self.client.get(reverse('message_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'message_list.html')
        self.assertContains(response, 'Test Subject')

    def test_message_detail(self):
        response = self.client.get(reverse('message_detail', args=[self.message.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'message_detail.html')
        self.assertContains(response, 'Test Message')

    def test_message_create(self):
        response = self.client.post(reverse('message_create'), {
            'subject': 'New Test Subject',
            'message': 'New Test Message'
        })
        self.assertEqual(response.status_code, 302)  # Successful creation redirects to message list
        self.assertTrue(Message.objects.filter(subject='New Test Subject').exists())

    def test_message_update(self):
        response = self.client.post(reverse('message_update', args=[self.message.id]), {
            'subject': 'Updated Test Subject',
            'message': 'Updated Test Message'
        })
        self.assertEqual(response.status_code, 302)  # Successful update redirects to message list
        self.message.refresh_from_db()
        self.assertEqual(self.message.subject, 'Updated Test Subject')

    def test_message_delete(self):
        response = self.client.post(reverse('message_delete', args=[self.message.id]))
        self.assertEqual(response.status_code, 302)  # Successful deletion redirects to message list
        self.assertFalse(Message.objects.filter(id=self.message.id).exists())

class AllMessagesViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='password12345')
        self.user2 = User.objects.create_user(username='testuser2', password='password12345')
        self.message1 = Message.objects.create(sender=self.user1, subject='User1 Message', message='User1 Message Content')
        self.message2 = Message.objects.create(sender=self.user2, subject='User2 Message', message='User2 Message Content')

    def test_all_messages_view(self):
        response = self.client.get(reverse('all_messages'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_messages.html')
        self.assertContains(response, 'User1 Message')
        self.assertContains(response, 'User2 Message')

class HomeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password12345')
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username='testuser', password='password12345')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_message_send_from_home(self):
        response = self.client.post(reverse('home'), {
            'subject': 'Home Test Subject',
            'message': 'Home Test Message'
        })
        self.assertEqual(response.status_code, 302)  # Successful send redirects to home
        self.assertTrue(Message.objects.filter(subject='Home Test Subject').exists())

class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='ComplexPass123!')
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username='testuser', password='ComplexPass123!')

    def test_profile_update(self):
        response = self.client.post(reverse('profile'), {
            'bio': 'New bio',
            'location': 'New location',
            'birth_date': '2000-01-01',
            'phone_number': '1234567890'
        })
        self.assertEqual(response.status_code, 302)  # Successful update should redirect
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'New bio')
        self.assertEqual(self.profile.location, 'New location')
        self.assertEqual(self.profile.birth_date, datetime.date(2000, 1, 1))
        self.assertEqual(self.profile.phone_number, '1234567890')


class MessageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='ComplexPass123!')
        self.client.login(username='testuser', password='ComplexPass123!')

    def test_message_create(self):
        response = self.client.post(reverse('message_create'), {
            'subject': 'Test Subject',
            'message': 'Test message content.'
        })
        self.assertEqual(response.status_code, 302)  # Successful creation should redirect
        self.assertTrue(Message.objects.filter(subject='Test Subject', message='Test message content.').exists())
