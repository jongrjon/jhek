"""Migrate blog.Post from a boolean `published` flag to a four-value status enum,
and drop the single-author `Profile` indirection in favour of a direct FK to User.

Data migration preserves existing rows:
    published=True  -> status="public"
    published=False -> status="draft"
    Post.author (FK -> Profile) -> Post.author (FK -> User), via Profile.user.

If a Post exists with author=None (shouldn't, PROTECT), it is left unchanged and the
later AlterField(null=False) will fail loudly so it can be addressed manually.
"""

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def published_to_status(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    for post in Post.objects.all():
        post.status = "public" if post.published else "draft"
        post.save(update_fields=["status"])


def status_to_published(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    for post in Post.objects.all():
        post.published = post.status == "public"
        post.save(update_fields=["published"])


def profile_fk_to_user_fk(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    for post in Post.objects.all():
        if post.author_id:
            # old author FK still points at Profile
            Profile = apps.get_model("blog", "Profile")
            profile = Profile.objects.filter(pk=post.author_id).first()
            if profile is not None:
                post.author_user_id = profile.user_id
                post.save(update_fields=["author_user"])


def noop(apps, schema_editor):
    # Reverse path for a rename-ish is lossy; accept one-way migration of owner.
    return


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # 1. Introduce status, data-migrate from published, drop published.
        migrations.AddField(
            model_name="post",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("private", "Private"),
                    ("unlisted", "Unlisted"),
                    ("public", "Public"),
                ],
                default="draft",
                max_length=10,
            ),
        ),
        migrations.RunPython(published_to_status, status_to_published),
        migrations.RemoveField(model_name="post", name="published"),

        # 2. Replace Post.author (FK -> Profile) with Post.author (FK -> User).
        migrations.AddField(
            model_name="post",
            name="author_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="blog_posts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(profile_fk_to_user_fk, noop),
        migrations.RemoveField(model_name="post", name="author"),
        migrations.RenameField(
            model_name="post", old_name="author_user", new_name="author"
        ),
        migrations.AlterField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="blog_posts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),

        # 3. Tighten meta_description length and Post.Meta ordering.
        migrations.AlterField(
            model_name="post",
            name="meta_description",
            field=models.CharField(blank=True, max_length=160),
        ),
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ["-publish_date", "-date_created"]},
        ),
        migrations.AlterModelOptions(
            name="tag",
            options={"ordering": ["name"]},
        ),
        migrations.AlterField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(blank=True, related_name="posts", to="blog.Tag"),
        ),

        # 4. Remove Profile model.
        migrations.DeleteModel(name="Profile"),
    ]
