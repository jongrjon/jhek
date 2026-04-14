from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ItemType(models.TextChoices):
    EDUCATION = "ED", "Education"
    JOB = "JO", "Job"
    SEMINAR = "SE", "Seminar"


class Person(models.Model):
    """The CV subject. Private data — never exposed without auth."""

    name = models.CharField(max_length=80)
    # kt: Icelandic national ID ("kennitala"). Personal data; keep non-unique
    # so it isn't an implicit join key, and to avoid accidental enumeration.
    kt = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)

    intro_is = models.TextField(blank=True)
    intro_en = models.TextField(blank=True)
    hobbies_is = models.TextField(blank=True)
    hobbies_en = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "People"

    def __str__(self) -> str:
        return self.name


class CVItem(models.Model):
    item_type = models.CharField(max_length=2, choices=ItemType.choices)
    title_is = models.CharField(max_length=80)
    title_en = models.CharField(max_length=80)
    where_is = models.CharField(max_length=80)
    where_en = models.CharField(max_length=80)
    start = models.DateField()
    leave = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-start"]

    def __str__(self) -> str:
        return f"{self.get_item_type_display()}: {self.title_en}"


class Skill(models.Model):
    skill_name_is = models.CharField(max_length=50)
    skill_name_en = models.CharField(max_length=50)
    skill_level = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        default=3,
    )

    class Meta:
        ordering = ["-skill_level", "skill_name_en"]

    def __str__(self) -> str:
        return f"{self.skill_name_en} ({self.skill_level}/5)"


class Recommender(models.Model):
    name = models.CharField(max_length=80)
    workplace_is = models.CharField(max_length=80)
    workplace_en = models.CharField(max_length=80)
    title_is = models.CharField(max_length=80)
    title_en = models.CharField(max_length=80)
    email = models.CharField(max_length=80, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} — {self.workplace_en}"


class ItemPoint(models.Model):
    item = models.ForeignKey(
        CVItem, on_delete=models.CASCADE, related_name="points"
    )
    text_is = models.TextField(blank=True)
    text_en = models.TextField(blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.item} — {self.text_en[:40]}"
