# Generated by Django 3.1.7 on 2021-03-23 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_auto_20210312_0054"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicallegalperson",
            name="deleted",
            field=models.BooleanField(
                blank=True, default=False, verbose_name="Deleted"
            ),
        ),
        migrations.AddField(
            model_name="historicalnaturalperson",
            name="deleted",
            field=models.BooleanField(
                blank=True, default=False, verbose_name="Deleted"
            ),
        ),
        migrations.AddField(
            model_name="historicalperson",
            name="deleted",
            field=models.BooleanField(
                blank=True, default=False, verbose_name="Deleted"
            ),
        ),
        migrations.AddField(
            model_name="historicalpersonassociation",
            name="deleted",
            field=models.BooleanField(
                blank=True, default=False, verbose_name="Deleted"
            ),
        ),
        migrations.AddField(
            model_name="person",
            name="deleted",
            field=models.BooleanField(
                blank=True, default=False, verbose_name="Deleted"
            ),
        ),
    ]