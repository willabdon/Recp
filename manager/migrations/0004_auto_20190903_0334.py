# Generated by Django 2.2.5 on 2019-09-03 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_auto_20190903_0333'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('article_number',)},
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='article_number',
            field=models.IntegerField(unique=True),
        ),
    ]