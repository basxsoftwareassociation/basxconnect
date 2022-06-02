# Generated by Django 4.0.5 on 2022-06-02 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20220602_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.person'),
        ),
        migrations.AlterField(
            model_name='email',
            name='type',
            field=models.ForeignKey(blank=True, limit_choices_to={'vocabulary__slug': 'emailtype'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type_%(app_label)s_%(class)s_list', to='core.term'),
        ),
        migrations.AlterField(
            model_name='fax',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.person'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.person'),
        ),
        migrations.AlterField(
            model_name='postal',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.person'),
        ),
        migrations.AlterField(
            model_name='postal',
            name='type',
            field=models.ForeignKey(blank=True, limit_choices_to={'vocabulary__slug': 'addresstype'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type_%(app_label)s_%(class)s_list', to='core.term'),
        ),
        migrations.AlterField(
            model_name='web',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.person'),
        ),
        migrations.AlterField(
            model_name='web',
            name='type',
            field=models.ForeignKey(blank=True, limit_choices_to={'vocabulary__slug': 'urltype'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type_%(app_label)s_%(class)s_list', to='core.term'),
        ),
    ]
