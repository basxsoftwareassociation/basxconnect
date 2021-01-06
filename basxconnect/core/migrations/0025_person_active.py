# Generated by Django 3.1.5 on 2021-01-06 11:30

from django.db import migrations, models


class Migration(migrations.Migration):
    def active_field(apps, _):
        Person = apps.get_model("core.Person")
        for person in Person.objects.all():
            person.active = not person.deleted
            person.save()

    dependencies = [
        ("core", "0024_auto_20210105_1955"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="active",
            field=models.BooleanField(default=True, verbose_name="Active"),
        ),
        migrations.RunPython(active_field, migrations.RunPython.noop),
    ]
