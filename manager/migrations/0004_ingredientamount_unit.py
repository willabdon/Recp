# Generated by Django 2.2.4 on 2019-08-31 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_auto_20190831_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientamount',
            name='unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='manager.Unit'),
            preserve_default=False,
        ),
    ]
