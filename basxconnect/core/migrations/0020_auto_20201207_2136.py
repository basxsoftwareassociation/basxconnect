# Generated by Django 3.1.4 on 2020-12-07 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_auto_20201207_2119"),
    ]

    operations = [
        migrations.AlterField(
            model_name="naturalperson",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True, verbose_name="Date of Birth"),
        ),
    ]