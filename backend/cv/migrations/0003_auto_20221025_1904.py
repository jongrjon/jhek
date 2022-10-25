# Generated by Django 3.2.14 on 2022-10-25 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv', '0002_auto_20220907_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cvitem',
            name='title_en',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='cvitem',
            name='title_is',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='cvitem',
            name='where_en',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='cvitem',
            name='where_is',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='reccommendor',
            name='email',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='reccommendor',
            name='title_en',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='reccommendor',
            name='title_is',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='reccommendor',
            name='workplace_en',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='reccommendor',
            name='workplace_is',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='skill',
            name='skill_name_en',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='skill',
            name='skill_name_is',
            field=models.CharField(max_length=30),
        ),
    ]
