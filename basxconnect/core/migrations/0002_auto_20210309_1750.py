# Generated by Django 3.1.5 on 2021-03-09 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="categories",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={"category__slug": "category"},
                to="core.Term",
            ),
        ),
    ]