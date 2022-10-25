from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now

TYPE = [
        ('ED', 'Education'),
        ('JO', 'Job'),
        ('SE', 'Seminar')
 ]

class Person(models.Model):
    name = models.CharField(max_length = 80)
    kt = models.CharField(max_length = 10, unique = True)
    phone = models.CharField(max_length = 15, null = True, blank = True)
    email = models.CharField(max_length = 50, null = True, blank = True)
    address = models.CharField(max_length = 50, null = True, blank = True)
    city = models.CharField(max_length = 50, null = True, blank = True)
    intro_is = models.TextField()
    intro_en = models.TextField()
    hobbies_is = models.TextField()
    hobbies_en = models.TextField()

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.name} ({self.kt})'

class CVItem(models.Model):
    item_type = models.CharField(max_length = 2, choices = TYPE)
    title_is = models.CharField(max_length = 50)
    title_en = models.CharField(max_length = 50)
    where_is = models.CharField(max_length = 50)
    where_en = models.CharField(max_length = 50)
    start = models.DateTimeField()
    leave = models.DateTimeField(null = True, blank = True)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.title_en}'

class Skill(models.Model):
    skill_name_is = models.CharField(max_length = 30)
    skill_name_en = models.CharField(max_length = 30)
    skill_level = models.IntegerField(validators = [MaxValueValidator(5), MinValueValidator(1)], default = 3)

    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f'{self.skill_name_en} ({self.skill_level})'

class Reccommendor(models.Model):
    name = models.CharField(max_length = 80)
    workplace_is = models.CharField(max_length = 50)
    workplace_en = models.CharField(max_length = 50)
    title_is = models.CharField(max_length = 50)
    title_en = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 15)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.name} - {self.workplace_en}'

class ItemPoint(models.Model):
    item = models.ForeignKey(CVItem, on_delete = models.PROTECT)
    text_is = models.TextField()
    text_en = models.TextField()

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.item} - {self.text_en}'