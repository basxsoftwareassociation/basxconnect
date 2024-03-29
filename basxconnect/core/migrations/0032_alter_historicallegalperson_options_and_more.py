# Generated by Django 4.0.6 on 2022-08-19 06:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0031_alter_email_person_alter_email_type_alter_fax_person_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="historicallegalperson",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Legal Person",
                "verbose_name_plural": "historical Legal Persons",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalnaturalperson",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Natural Person",
                "verbose_name_plural": "historical Natural Persons",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalperson",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Person",
                "verbose_name_plural": "historical Persons",
            },
        ),
        migrations.AlterModelOptions(
            name="historicalpersonassociation",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Person Association",
                "verbose_name_plural": "historical Person Associations",
            },
        ),
        migrations.AlterField(
            model_name="historicallegalperson",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalnaturalperson",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalperson",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name="historicalpersonassociation",
            name="history_date",
            field=models.DateTimeField(db_index=True),
        ),
    ]
