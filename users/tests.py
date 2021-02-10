from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse, resolve

from users.forms import CustomUserCreationForm
from users.views import SignupPageView


class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="Igor",
            email="b@b.pl",
            password="testpass123"
        )

        #   asercje (ify z roznymi conditions)
        self.assertEqual(user.username, "Igor")
        self.assertEqual(user.email, "b@b.pl")
        self.assertTrue(user.is_active)
        # email send by app to user to confirm and when he confirmed he/she status will be in active
        self.assertFalse(user.is_staff)  # czy jest modem
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="superadmin",
            email="b@b.pl",
            password="testpass123"
        )

        self.assertEqual(admin_user.username, "superadmin")
        self.assertEqual(admin_user.email, "b@b.pl")
        self.assertTrue(admin_user.is_active)
        # email send by app to user to confirm and when he confirmed he/she status will be in active
        self.assertTrue(admin_user.is_staff)  # czy jest modem
        self.assertTrue(admin_user.is_superuser)


class SignupPageTests(TestCase):
    username = 'newuser'
    email = 'newuser@email.com'
    # ficture
    # start before tests
    def setUp(self):
        url = reverse('account_signup')  # pobieranie url  po nazwie
        self.response = self.client.get(url)  # ten get sie nie odbywa to zostaje zmocokowane - tylko makieta podana
        # w unit t estach nie ma side effect - wiec nie pytamy o response url tylko
        # ten client nie pyta wprost tylko client.get(url) symuluje

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/signup.html')
        self.assertContains(self.response, 'Sign')
        self.assertNotContains(self.response, 'Log')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(
            self.username, self.email
        )
        # to co komentowane to bylo przed wprowadziem all aouth i np testuja funkcjonalnosci all auth
        #sprawdzam ile stworzylo sie w bazie userow
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)
        # form = self.response.context.get('form')
        # kazda templatka ma context wiec mozemy z niego wyciagnac form
        # self.assertIsInstance(form, CustomUserCreationForm)
        # self.assertContains(self.response, 'csrfmiddlewaretoken') #csrf token

    # def test_signup_view(self):
    #     view = resolve('/accounts/signup/') # resolve przeciwna do reverse dostaje endpoint a zwraca funkcje
    #     self.assertEqual(
    #         view.func.__name__,
    #         SignupPageView.as_view().__name__
    #         )