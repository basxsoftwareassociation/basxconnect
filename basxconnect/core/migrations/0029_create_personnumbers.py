# Generated by Django 3.1.5 on 2021-01-11 10:57

from django.db import migrations


class Migration(migrations.Migration):
    def save(apps, _):
        for person in apps.get_model("core.Person").objects.all():
            person.personnumber = str(person.pk)
            person.save()  # save will generate the personnumber automatically

    dependencies = [
        ("core", "0028_auto_20210111_1753"),
    ]

    operations = [migrations.RunPython(save, migrations.RunPython.noop)]