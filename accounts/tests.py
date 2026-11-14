
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountTests(TestCase):
    def test_registration_page(self):
        response = self.client.get(
            reverse("accounts:register")
        )
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "testbuyer",
                "email": "buyer@example.com",
                "password1": "StrongTestPassword123!",
                "password2": "StrongTestPassword123!",
            },
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_duplicate_email(self):
        User.objects.create_user(
            username="firstbuyer",
            email="buyer@example.com",
            password="StrongTestPassword123!",
        )

        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "secondbuyer",
                "email": "buyer@example.com",
                "password1": "StrongTestPassword123!",
                "password2": "StrongTestPassword123!",
            },
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(
            reverse("accounts:login")
        )
        self.assertEqual(response.status_code, 200)
