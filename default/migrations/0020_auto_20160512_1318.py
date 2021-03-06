# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-12 13:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0019_auto_20160216_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='secao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_secao', to='default.Secao', verbose_name='Nova Se\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='material',
            name='secoes_possiveis',
            field=models.ManyToManyField(blank=True, to='default.Secao', verbose_name='Se\xe7\xf5es Possiveis'),
        ),
    ]
