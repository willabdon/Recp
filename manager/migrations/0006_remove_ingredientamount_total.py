# Generated by Django 2.2.5 on 2019-09-04 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_auto_20190903_2334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredientamount',
            name='total',
        ),
    ]