# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-09 11:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Arc', '0004_auto_20161209_0848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='own',
            name='id',
        ),
        migrations.AlterField(
            model_name='own',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='book_own', serialize=False, to='Arc.book'),
        ),
        migrations.AlterField(
            model_name='own',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_own', to='Arc.ArcUser'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wantgoods', to='Arc.book'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='sno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whocart', to='Arc.ArcUser'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trade_goods', to='Arc.book'),
        ),
    ]