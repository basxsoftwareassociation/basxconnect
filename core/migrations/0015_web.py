# Generated by Django 3.1 on 2020-11-21 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20201121_1003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Web',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='Url')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_web_list', to='core.person')),
                ('status', models.ForeignKey(help_text='eg. active, moved, inactive', limit_choices_to={'category__slug': 'addressstatus'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='status_core_web_list', to='core.term')),
                ('type', models.ForeignKey(help_text='eg. Private, Business', limit_choices_to={'category__slug': 'addresstype'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type_core_web_list', to='core.term')),
            ],
            options={
                'verbose_name': 'Web address',
                'verbose_name_plural': 'Web addresses',
            },
        ),
    ]
