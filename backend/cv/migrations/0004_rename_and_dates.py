"""Rename Reccommendor -> Recommender, convert CVItem.start/leave to DateField,
relax Person.kt (no longer unique), blank=True on contact fields, extend string
lengths to match new models. ItemPoint.item cascades now.

Converting DateTimeField -> DateField truncates the time component. That's
intentional: the CV template only ever formatted as m/Y.
"""

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cv", "0003_auto_20221025_1904"),
    ]

    operations = [
        # Rename the misspelled model.
        migrations.RenameModel(old_name="Reccommendor", new_name="Recommender"),

        # CVItem: dates and longer titles.
        migrations.AlterField(
            model_name="cvitem",
            name="start",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="cvitem",
            name="leave",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="cvitem",
            name="title_is",
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name="cvitem",
            name="title_en",
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name="cvitem",
            name="where_is",
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name="cvitem",
            name="where_en",
            field=models.CharField(max_length=80),
        ),
        migrations.AlterModelOptions(
            name="cvitem",
            options={"ordering": ["-start"]},
        ),

        # Person: kt no longer unique; text contacts use blank="" rather than NULL.
        migrations.AlterField(
            model_name="person",
            name="kt",
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name="person",
            name="phone",
            field=models.CharField(blank=True, default="", max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="person",
            name="email",
            field=models.CharField(blank=True, default="", max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="person",
            name="address",
            field=models.CharField(blank=True, default="", max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="person",
            name="city",
            field=models.CharField(blank=True, default="", max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="person",
            name="intro_is",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="intro_en",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="hobbies_is",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="hobbies_en",
            field=models.TextField(blank=True),
        ),
        migrations.AlterModelOptions(
            name="person",
            options={"verbose_name_plural": "People"},
        ),

        # Skill: longer names + ordering.
        migrations.AlterField(
            model_name="skill",
            name="skill_name_is",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="skill",
            name="skill_name_en",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterModelOptions(
            name="skill",
            options={"ordering": ["-skill_level", "skill_name_en"]},
        ),

        # Recommender: longer fields, blanks, ordering.
        migrations.AlterField(
            model_name="recommender",
            name="workplace_is",
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name="recommender",
            name="workplace_en",
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name="recommender",
            name="title_is",
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name="recommender",
            name="title_en",
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name="recommender",
            name="email",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AlterField(
            model_name="recommender",
            name="phone",
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterModelOptions(
            name="recommender",
            options={"ordering": ["name"]},
        ),

        # ItemPoint: cascade deletes + related_name, blank text.
        migrations.AlterField(
            model_name="itempoint",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="points",
                to="cv.cvitem",
            ),
        ),
        migrations.AlterField(
            model_name="itempoint",
            name="text_is",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="itempoint",
            name="text_en",
            field=models.TextField(blank=True),
        ),
        migrations.AlterModelOptions(
            name="itempoint",
            options={"ordering": ["id"]},
        ),
    ]
