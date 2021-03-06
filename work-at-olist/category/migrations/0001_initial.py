# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 06:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('channel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=260, populate_from='name', verbose_name='Slug')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='channel.Channel', verbose_name='Channel')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
    ]
