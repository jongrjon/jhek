from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Status(models.TextChoices):
    """Blog post visibility.

    DRAFT:    author only; never served publicly.
    PRIVATE:  logged-in site owner only.
    UNLISTED: reachable by slug; not listed; marked noindex.
    PUBLIC:   listed and reachable.
    """

    DRAFT = "draft", "Draft"
    PRIVATE = "private", "Private"
    UNLISTED = "unlisted", "Unlisted"
    PUBLIC = "public", "Public"


class PostQuerySet(models.QuerySet):
    def public(self):
        return self.filter(status=Status.PUBLIC)

    def unlisted(self):
        return self.filter(status=Status.UNLISTED)

    def listed(self):
        """Posts that may appear in lists."""
        return self.public()

    def visible_to(self, user):
        """Single authority on who can see what."""
        if user.is_authenticated and user.is_staff:
            return self.all()
        if user.is_authenticated:
            # Logged-in owner sees public + private + unlisted (if they own it).
            return self.filter(
                models.Q(status=Status.PUBLIC)
                | models.Q(status=Status.UNLISTED)
                | models.Q(status=Status.PRIVATE, author=user)
            )
        # Anonymous: only public + direct unlisted links (handled in views).
        return self.filter(status=Status.PUBLIC)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("blog:tag", args=[self.name])


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    body = models.TextField()
    meta_description = models.CharField(max_length=160, blank=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    publish_date = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="blog_posts",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["-publish_date", "-date_created"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("blog:detail", args=[self.slug])

    def save(self, *args, **kwargs):
        # Stamp publish_date the first time a post leaves draft.
        if self.status != Status.DRAFT and self.publish_date is None:
            self.publish_date = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_listed(self) -> bool:
        return self.status == Status.PUBLIC

    @property
    def is_indexable(self) -> bool:
        return self.status == Status.PUBLIC
