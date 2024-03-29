# Generated by Django 4.1.7 on 2023-04-03 06:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0035_alter_email_type_alter_fax_type_and_more"),
        ("basxconnect_projects", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="client",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="projects",
                to="core.person",
                verbose_name="Client",
            ),
        ),
    ]
