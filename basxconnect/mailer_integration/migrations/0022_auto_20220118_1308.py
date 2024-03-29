# Generated by Django 3.2.4 on 2022-01-18 12:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mailer_integration", "0021_auto_20220106_0917"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscription",
            name="active",
        ),
        migrations.AddField(
            model_name="subscription",
            name="status_before_archiving",
            field=models.CharField(
                choices=[
                    ("subscribed", "subscribed"),
                    ("unsubscribed", "unsubscribed"),
                    ("non-subscribed", "non-subscribed"),
                    ("cleaned", "cleaned"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="status",
            field=models.CharField(
                choices=[
                    ("subscribed", "subscribed"),
                    ("unsubscribed", "unsubscribed"),
                    ("non-subscribed", "non-subscribed"),
                    ("cleaned", "cleaned"),
                    ("archived", "archived"),
                ],
                max_length=50,
            ),
        ),
    ]
