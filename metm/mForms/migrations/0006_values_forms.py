# Generated by Django 3.1.2 on 2020-10-27 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mForms', '0005_auto_20201027_0318'),
    ]

    operations = [
        migrations.AddField(
            model_name='values',
            name='forms',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='values', to='mForms.forms', verbose_name='Forms'),
        ),
    ]
