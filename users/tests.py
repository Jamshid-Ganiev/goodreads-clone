from django.test import TestCase
from users.models import CustomUser
from django.urls import reverse
from django.contrib.auth import get_user


# Create your tests here.
class SignUpTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:signup"),
            data = {
                "username": 'jamshid3',
                "first_name": 'jamshid',
                "last_name": 'ganiev',
                "email": 'jamwid@mail.ru',
                "password": "somepassword"
            }
        )

        user = CustomUser.objects.get(username="jamshid3")

        self.assertEqual(user.first_name, "jamshid")
        self.assertEqual(user.last_name, "ganiev")
        self.assertEqual(user.email, "jamwid@mail.ru")
        self.assertNotEqual(user.password, "somepassword")
        self.assertTrue(user.check_password("somepassword"))


    def test_required_fields(self):
        """ Required field bo'lgan joylarni to'ldirmasdan submit qilganimizda, register qilmanaganligini tekshirish uchun test."""
        response = self.client.post(
            reverse("users:signup"),
            data={
                "first_name": 'jamshid',
                "email": 'jamwid@mail.ru'
            }
        )

        user_count = CustomUser.objects.count()
        # required field ni to'ldirmay submit qilganimizda ba'zada shunday user yaratilmagan bo'aldi va 0 ga teng bo'ladi, shuni test qilamiz
        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")


    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:signup"),
            data={
                "username": 'jamshid3',
                "first_name": 'jamshid',
                "last_name": 'ganiev',
                "email": 'invalid_email',
                "password": "somepassword"
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)

        self.assertFormError(response, 'form', "email", 'Enter a valid email address.')


    def test_unique_username(self):
        # MY METHOD:
        # self.client.post(
        #     reverse("users:register"),
        #     data={
        #         "username": 'jamshid3',
        #         "first_name": 'jamshid',
        #         "last_name": 'ganiev',
        #         "email": 'jamwid@mail.ru',
        #         "password": "somepassword"
        #     }
        # )

        # KAHOGI's METHOD:
        user = CustomUser.objects.create(username='jamshid3', first_name='jamshid')
        user.set_password("somepasswordd")
        user.save()

        #Create a username with that same username
        response = self.client.post(
            reverse("users:signup"),
            data={
                "username": 'jamshid3',
                "first_name": 'jamshidd',
                "last_name": 'ganievv',
                "email": 'jjamwid@mail.ru',
                "password": "ssomepassword"
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')


class LoginTestCase(TestCase):
    def setUp(self):
        """ DRY--> Don't Repeat Yourself"""
        self.db_user = CustomUser.objects.create(username='james', first_name='Jamshid')
        self.db_user.set_password('password77')
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": 'james',
                'password': 'password77'
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse("users:login"),
            data={
                "username": 'wrong-username',
                'password': 'password77'
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("users:login"),
            data={
                "username": 'james',
                'password': 'wrong-password'
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username='james', password='password77')

        self.client.get(reverse("users:logout"))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        # just an additional test case by using status code this time
        self.assertEqual(response.status_code, 302)

        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username= 'james',
            first_name= 'Jamshid',
            last_name= 'Ganiev',
            email = 'james@gmail.com'
        )
        user.set_password('strongpassword')
        user.save()

        # easier way of login in tests is just to use login method of client itself
        self.client.login(username= 'james', password='strongpassword')

        response = self.client.get(reverse("users:profile"))

        # just an additional test case by using status code this time
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username='james', first_name='Jamshid', last_name='Ganiev', email='james@gmail.com'
        )
        user.set_password('password00')
        user.save()

        self.client.login(username='james', password='password00')

        response = self.client.post(
            reverse("users:profile-edit"),
            data={
                "username": "james77",
                "first_name": "Jamshidjon",
                "last_name": "Ganiev",
                "email": "jganiev@gmail.com"
            }
        )
        user.refresh_from_db()

        self.assertEqual(user.username, "james77")
        self.assertEqual(user.email, "jganiev@gmail.com")
        self.assertEqual(response.url, reverse("users:profile"))
