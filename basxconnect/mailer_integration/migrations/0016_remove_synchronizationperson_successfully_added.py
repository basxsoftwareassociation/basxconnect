# Generated by Django 3.2.4 on 2021-11-22 09:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("mailer_integration", "0015_synchronizationperson_message"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="synchronizationperson",
            name="successfully_added",
        ),
    ]
