# Generated by Django 3.1.1 on 2020-10-19 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='type',
            field=models.ForeignKey(help_text='eg. private, business', limit_choices_to={'category__slug': 'addresstype'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='core_email_type', to='core.term'),
        ),
        migrations.AlterField(
            model_name='legalperson',
            name='type',
            field=models.ForeignKey(help_text='eg. Church, Business, Association', limit_choices_to={'category__slug': 'legaltype'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='legaltype', to='core.term'),
        ),
        migrations.AlterField(
            model_name='person',
            name='abbreviation_key',
            field=models.CharField(blank=True, help_text='abbreviation of the name, for quick search of persons', max_length=255, verbose_name='Abbreviation'),
        ),
        migrations.AlterField(
            model_name='person',
            name='connect_key',
            field=models.CharField(blank=True, help_text='This key can be communicated publically', max_length=255, verbose_name='Connect Key'),
        ),
        migrations.AlterField(
            model_name='person',
            name='legacy_key',
            field=models.CharField(blank=True, max_length=255, verbose_name='Legacy Key'),
        ),
        migrations.AlterField(
            model_name='pobox',
            name='pobox_city',
            field=models.TextField(blank=True, verbose_name='POBox City'),
        ),
        migrations.AlterField(
            model_name='pobox',
            name='pobox_name',
            field=models.TextField(blank=True, verbose_name='POBox Name'),
        ),
        migrations.AlterField(
            model_name='pobox',
            name='pobox_postcode',
            field=models.TextField(blank=True, verbose_name='POBox Post Code'),
        ),
        migrations.AlterField(
            model_name='pobox',
            name='type',
            field=models.ForeignKey(help_text='eg. private, business', limit_choices_to={'category__slug': 'addresstype'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='core_pobox_type', to='core.term'),
        ),
        migrations.AlterField(
            model_name='postal',
            name='city',
            field=models.TextField(blank=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='postal',
            name='postcode',
            field=models.TextField(blank=True, verbose_name='Post Code'),
        ),
        migrations.AlterField(
            model_name='postal',
            name='supplemental_address',
            field=models.TextField(blank=True, verbose_name='Supplemental Address'),
        ),
        migrations.AlterField(
            model_name='postal',
            name='type',
            field=models.ForeignKey(help_text='eg. private, business', limit_choices_to={'category__slug': 'addresstype'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='core_postal_type', to='core.term'),
        ),
        migrations.DeleteModel(
            name='AddressType',
        ),
        migrations.DeleteModel(
            name='LegalType',
        ),
    ]