# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-03 13:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0013_secaosap'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='secaosap',
            options={'ordering': ['cod_secao'], 'verbose_name': 'Se\xe7\xe3o SAP', 'verbose_name_plural': 'Se\xe7\xf5es SAP'},
        ),
        migrations.RemoveField(
            model_name='material',
            name='secao',
        ),
        migrations.AddField(
            model_name='secaosap',
            name='secoes_destino_possiveis',
            field=models.ManyToManyField(to='default.Secao', verbose_name='Se\xe7\xf5es Novas Possiveis'),
        ),
        migrations.RemoveField(
            model_name='material',
            name='secoes_possiveis',
        ),
        migrations.AddField(
            model_name='material',
            name='secoes_possiveis',
            field=models.ManyToManyField(to='default.Secao', verbose_name='Se\xe7\xf5es Possiveis'),
        ),
    ]