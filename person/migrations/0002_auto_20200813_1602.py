# Generated by Django 3.1 on 2020-08-13 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='relationship',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Ends on'),
        ),
        migrations.AddField(
            model_name='relationship',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Starts on'),
        ),
    ]