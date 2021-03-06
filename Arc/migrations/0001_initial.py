# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-08 15:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArcUser',
            fields=[
                ('sno', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=20)),
                ('passwd', models.CharField(max_length=20)),
                ('sex', models.CharField(max_length=4)),
                ('dept', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('totalbought', models.IntegerField()),
                ('totalsell', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='book',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, serialize=False)),
                ('bname', models.CharField(max_length=20)),
                ('author', models.CharField(max_length=20)),
                ('publisher', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quality', models.IntegerField()),
                ('bimg', models.CharField(max_length=50)),
                ('discp', models.CharField(max_length=200)),
                ('bclass', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='own',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Arc.book')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Arc.ArcUser')),
            ],
        ),
        migrations.CreateModel(
            name='shoppingcart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Arc.book')),
                ('sno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Arc.ArcUser')),
            ],
        ),
        migrations.CreateModel(
            name='trade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statu', models.IntegerField()),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whoBuy', to='Arc.ArcUser')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Arc.book')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whoSell', to='Arc.ArcUser')),
            ],
        ),
        migrations.CreateModel(
            name='unverified',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Arc.ArcUser')),
            ],
        ),
    ]
