# Generated by Django 3.1.5 on 2021-01-12 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0034_auto_20210112_1106"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicallegalperson",
            name="remarks",
            field=models.TextField(blank=True, verbose_name="Remarks"),
        ),
        migrations.AddField(
            model_name="historicalnaturalperson",
            name="remarks",
            field=models.TextField(blank=True, verbose_name="Remarks"),
        ),
        migrations.AddField(
            model_name="historicalperson",
            name="remarks",
            field=models.TextField(blank=True, verbose_name="Remarks"),
        ),
        migrations.AddField(
            model_name="historicalpersonassociation",
            name="remarks",
            field=models.TextField(blank=True, verbose_name="Remarks"),
        ),
        migrations.AddField(
            model_name="person",
            name="remarks",
            field=models.TextField(blank=True, verbose_name="Remarks"),
        ),
        migrations.AlterField(
            model_name="postal",
            name="address",
            field=models.TextField(blank=True, verbose_name="Address"),
        ),
    ]