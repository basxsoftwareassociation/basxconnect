# Generated by Django 3.1.7 on 2021-05-23 04:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_auto_20210522_1817"),
    ]

    operations = [
        migrations.AlterField(
            model_name="email",
            name="type",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={"category__slug": "emailtype"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="type_core_email_list",
                to="core.term",
            ),
        ),
    ]
