# Generated by Django 3.1.5 on 2021-02-10 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_auto_20210210_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postal',
            name='address',
            field=models.TextField(blank=True, verbose_name='Address'),
        ),
    ]