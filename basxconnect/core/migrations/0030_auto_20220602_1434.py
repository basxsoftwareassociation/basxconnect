# Generated by Django 3.2.13 on 2022-06-02 07:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0029_auto_20220429_1138"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalnaturalperson",
            name="place_of_birth",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Place of Birth"
            ),
        ),
        migrations.AddField(
            model_name="naturalperson",
            name="place_of_birth",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Place of Birth"
            ),
        ),
    ]
