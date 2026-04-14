from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Post, Status

User = get_user_model()


class PostVisibilityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="author", password="x")
        cls.draft = Post.objects.create(
            title="D", slug="d", body="b", status=Status.DRAFT, author=cls.author
        )
        cls.private = Post.objects.create(
            title="Priv", slug="priv", body="b", status=Status.PRIVATE, author=cls.author
        )
        cls.unlisted = Post.objects.create(
            title="U", slug="u", body="b", status=Status.UNLISTED, author=cls.author
        )
        cls.public = Post.objects.create(
            title="P", slug="p", body="b", status=Status.PUBLIC, author=cls.author
        )

    def test_list_shows_only_public(self):
        resp = self.client.get(reverse("blog:list"))
        self.assertContains(resp, "P")
        self.assertNotContains(resp, ">U<")
        self.assertNotContains(resp, "Priv")
        self.assertNotContains(resp, ">D<")

    def test_draft_is_404_for_anonymous(self):
        resp = self.client.get(reverse("blog:detail", args=["d"]))
        self.assertEqual(resp.status_code, 404)

    def test_private_is_404_for_anonymous(self):
        resp = self.client.get(reverse("blog:detail", args=["priv"]))
        self.assertEqual(resp.status_code, 404)

    def test_unlisted_is_200_for_anonymous(self):
        resp = self.client.get(reverse("blog:detail", args=["u"]))
        self.assertEqual(resp.status_code, 200)

    def test_public_is_200_for_anonymous(self):
        resp = self.client.get(reverse("blog:detail", args=["p"]))
        self.assertEqual(resp.status_code, 200)

    def test_publish_date_stamped_on_first_non_draft_save(self):
        p = Post.objects.create(
            title="X", slug="x", body="b", status=Status.DRAFT, author=self.author
        )
        self.assertIsNone(p.publish_date)
        p.status = Status.PUBLIC
        p.save()
        self.assertIsNotNone(p.publish_date)
