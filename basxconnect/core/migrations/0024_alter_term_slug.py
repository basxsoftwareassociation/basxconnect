# Generated by Django 3.2.5 on 2021-11-24 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0023_auto_20211030_0955"),
    ]

    operations = [
        migrations.AlterField(
            model_name="term",
            name="slug",
            field=models.CharField(blank=True, max_length=255, verbose_name="Slug"),
        ),
    ]