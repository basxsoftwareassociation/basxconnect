# Generated by Django 3.2.5 on 2021-11-24 08:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0024_alter_term_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="term",
            name="slug",
            field=models.CharField(
                blank=True, max_length=255, unique=True, verbose_name="Slug"
            ),
        ),
    ]
