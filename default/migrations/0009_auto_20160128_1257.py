# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-28 12:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0008_auto_20160121_2103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='multiplas_familias_selecionadas',
        ),
        migrations.RemoveField(
            model_name='sugestao',
            name='selecionado',
        ),
        migrations.AlterField(
            model_name='material',
            name='familia',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='default.Familia', verbose_name='Familia'),
        ),
        migrations.AlterField(
            model_name='material',
            name='familia_selecionada',
            field=models.BooleanField(default=False, verbose_name='Familia Selecionada'),
        ),
        migrations.AlterField(
            model_name='material',
            name='familia_sugerida',
            field=models.BooleanField(default=False, verbose_name='Familia Sugerida'),
        ),
        migrations.AlterField(
            model_name='material',
            name='secao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_secao', to='default.Secao', verbose_name='Se\xe7\xe3o'),
        ),
        migrations.AlterField(
            model_name='sugestao',
            name='score',
            field=models.FloatField(default=0, verbose_name='Pontua\xe7\xe3o'),
        ),
    ]
