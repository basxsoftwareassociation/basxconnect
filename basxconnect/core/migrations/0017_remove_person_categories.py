# Generated by Django 3.2.5 on 2021-09-28 10:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_auto_20210928_1534"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="person",
            name="categories",
        ),
    ]
