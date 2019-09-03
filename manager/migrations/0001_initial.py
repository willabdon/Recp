# Generated by Django 2.2.5 on 2019-09-03 00:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('article_number', models.CharField(max_length=200, unique=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_ingredients', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IngredientAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.PositiveSmallIntegerField(choices=[(1, 'kg'), (2, 'g'), (3, 'l'), (4, 'cl')], primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_recipes', to=settings.AUTH_USER_MODEL)),
                ('ingredients', models.ManyToManyField(through='manager.IngredientAmount', to='manager.Ingredient')),
            ],
        ),
        migrations.AddField(
            model_name='ingredientamount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Recipe'),
        ),
        migrations.AddField(
            model_name='ingredientamount',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Unit'),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.Unit'),
        ),
    ]
