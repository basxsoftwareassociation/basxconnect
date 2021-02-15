# Generated by Django 3.1 on 2020-11-24 06:21

from django.db import migrations


class Migration(migrations.Migration):
    def create_category(apps, schema_editor):
        Category = apps.get_model("core.Category")
        Term = apps.get_model("core.Term")
        if not Category.objects.filter(slug="associationtype").exists():
            cat = Category.objects.create(
                name="Association Type", slug="associationtype"
            )
        else:
            cat = Category.objects.filter(slug="associationtype").first()
        Term.objects.create(term="Household", category=cat)

    dependencies = [
        ("core", "0016_add_address_origin"),
    ]

    operations = [migrations.RunPython(create_category, migrations.RunPython.noop)]
