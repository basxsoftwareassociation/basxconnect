# Generated by Django 3.2.4 on 2021-08-25 08:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_auto_20210726_2047"),
        ("mailer_integration", "0007_alter_mailingpreferences_interests"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailingpreferences",
            name="email",
            field=models.OneToOneField(
                blank=True, on_delete=django.db.models.deletion.CASCADE, to="core.email"
            ),
        ),
    ]
