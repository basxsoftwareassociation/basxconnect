# Generated by Django 3.2.4 on 2021-08-23 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_auto_20210726_2047"),
        ("mailer_integration", "0003_alter_interest_external_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mailingpreferences",
            name="person",
        ),
        migrations.AddField(
            model_name="mailingpreferences",
            name="email",
            field=models.OneToOneField(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.person",
            ),
            preserve_default=False,
        ),
    ]
