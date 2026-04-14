from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class CVAccessTests(TestCase):
    def test_anonymous_is_redirected_to_login(self):
        resp = self.client.get(reverse("cv:html"))
        self.assertEqual(resp.status_code, 302)

    def test_staff_can_access(self):
        User.objects.create_user(
            username="owner", password="x", is_staff=True
        )
        self.client.login(username="owner", password="x")
        resp = self.client.get(reverse("cv:html"))
        self.assertEqual(resp.status_code, 200)
