# Generated by Django 3.1.4 on 2020-12-15 08:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0022_auto_20201214_1755"),
    ]

    operations = [
        migrations.AlterField(
            model_name="email",
            name="status",
            field=models.ForeignKey(
                limit_choices_to={"category__slug": "addressstatus"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="status_core_email_list",
                to="core.term",
            ),
        ),
        migrations.AlterField(
            model_name="email",
            name="type",
            field=models.ForeignKey(
                limit_choices_to={"category__slug": "addresstype"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="type_core_email_list",
                to="core.term",
            ),
        ),
        migrations.AlterField(
            model_name="fax",
            name="status",
            field=models.ForeignKey(
                limit_choices_to={"category__slug": "addressstatus"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="status_core_fax_list",
                to="core.term",
            ),
        ),
        migrations.AlterField(
            model_name="fax",
            name="type",
            field=models.ForeignKey(
                limit_choices_to={"category__slug": "phonetype"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.term",
            ),
        ),
        migrations.AlterField(
            model_name="phone",
            name="status",
            field=models.ForeignKey(
                limit_choices_to={"category__slug": "addressstatus"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="status_core_phone_list",
                to="core.term",
            ),
        ),
        migrations.AlterField(
            model_name="phone",
            name="type",
            field=models.ForeignKey(
                limit_choices_to={"category__slug": "phonetype"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.term",
            ),
        ),
        migrations.AlterField(
            model_name="pobox",
            name="status",
            field=models.ForeignKey(
                limit_choices_to={"category__slug": "addressstatus"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="status_core_pobox_list",
                to="core.term",
            ),
        ),
        migrations.AlterField(
            model_name="pobox",
            name="type",
            field=models.ForeignKey(
                limit_choices_to={"category__slug": "addresstype"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="type_core_pobox_list",
                to="core.term",
            ),
        ),
        migrations.AlterField(
            model_name="postal",
            name="address",
            field=models.CharField(max_length=255, verbose_name="Address"),
        ),
        migrations.AlterField(
            model_name="postal",
            name="status",
            field=models.ForeignKey(
                limit_choices_to={"category__slug": "addressstatus"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="status_core_postal_list",
                to="core.term",
            ),
        ),
        migrations.AlterField(
            model_name="postal",
            name="type",
            field=models.ForeignKey(
                limit_choices_to={"category__slug": "addresstype"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="type_core_postal_list",
                to="core.term",
            ),
        ),
        migrations.AlterField(
            model_name="web",
            name="status",
            field=models.ForeignKey(
                limit_choices_to={"category__slug": "addressstatus"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="status_core_web_list",
                to="core.term",
            ),
        ),
        migrations.AlterField(
            model_name="web",
            name="type",
            field=models.ForeignKey(
                limit_choices_to={"category__slug": "addresstype"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="type_core_web_list",
                to="core.term",
            ),
        ),
    ]
