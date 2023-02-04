# Generated by Django 3.1.5 on 2021-03-11 11:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_auto_20210309_2221"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalnaturalperson",
            name="form_of_address",
        ),
        migrations.RemoveField(
            model_name="naturalperson",
            name="form_of_address",
        ),
        migrations.AlterField(
            model_name="historicalnaturalperson",
            name="decease_date",
            field=models.DateField(blank=True, null=True, verbose_name="Deceased Date"),
        ),
        migrations.AlterField(
            model_name="historicalnaturalperson",
            name="deceased",
            field=models.BooleanField(default=False, verbose_name="Deceased"),
        ),
        migrations.AlterField(
            model_name="naturalperson",
            name="decease_date",
            field=models.DateField(blank=True, null=True, verbose_name="Deceased Date"),
        ),
        migrations.AlterField(
            model_name="naturalperson",
            name="deceased",
            field=models.BooleanField(default=False, verbose_name="Deceased"),
        ),
        migrations.AlterField(
            model_name="naturalperson",
            name="salutation",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"category__slug": "salutation"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="core.term",
            ),
        ),
    ]
