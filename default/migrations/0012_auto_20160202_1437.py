# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-02 14:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0011_auto_20160202_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='secao',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_secao', to='default.Secao', verbose_name='Se\xe7\xe3o'),
        ),
    ]
