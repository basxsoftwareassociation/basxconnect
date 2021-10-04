# Generated by Django 3.2.5 on 2021-09-28 08:34

from django.db import migrations, models


class Migration(migrations.Migration):
    def copy_tags(apps, scheme_editor):
        for person in apps.get_model("core.Person").objects.all():
            person.tags.set(person.categories.all())
            person.save()

    dependencies = [
        ("core", "0015_rename_category_to_tag"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="tags",
            field=models.ManyToManyField(
                blank=True, limit_choices_to={"vocabulary__slug": "tag"}, to="core.Term"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="categories",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={"vocabulary__slug": "tag"},
                related_name="_core_person_categories_+",
                to="core.Term",
            ),
        ),
        migrations.RunPython(copy_tags, migrations.RunPython.noop),
    ]