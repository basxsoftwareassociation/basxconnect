# Generated by Django 3.2.4 on 2021-11-22 13:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mailer_integration", "0017_auto_20211122_1219"),
    ]

    operations = [
        migrations.AlterField(
            model_name="synchronizationperson",
            name="sync_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("new", "Newly added to BasxConnect"),
                    ("import_error", "Not added to BasxConnect"),
                    ("synced_previously", "Synchronized previously but not this time"),
                ],
                max_length=255,
                verbose_name="Synchronization Status",
            ),
        ),
    ]
