# Generated by Django 3.1 on 2020-11-21 10:03

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_juristicperson_name_addition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='juristicperson',
            name='name_addition',
            field=models.CharField(blank=True, max_length=255, verbose_name='Addition name'),
        ),
        migrations.CreateModel(
            name='Fax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Number')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_fax_list', to='core.person')),
                ('status', models.ForeignKey(help_text='eg. active, moved, inactive', limit_choices_to={'category__slug': 'addressstatus'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='status_core_fax_list', to='core.term')),
                ('type', models.ForeignKey(help_text='eg. Private, Business', limit_choices_to={'category__slug': 'phonetype'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.term')),
            ],
            options={
                'verbose_name': 'Fax number',
                'verbose_name_plural': 'Fax numbers',
            },
        ),
    ]