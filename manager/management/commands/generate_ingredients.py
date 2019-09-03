from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import IntegrityError

from apicbase.models import CustomUser
from manager.models import Unit, Ingredient


class Command(BaseCommand):
    help = 'Send test emails'

    def handle(self, *args, **options):
        ingredients = [
            {
                'article_number': '001',
                'name': 'Kiwi',
                'value': 4,
                'amount': 1,
                'unit': Unit.KILOGRAM
            },
            {
                'article_number': '002',
                'name': 'Strawberry',
                'value': 3,
                'amount': 1,
                'unit': Unit.KILOGRAM
            },
            {
                'article_number': '003',
                'name': 'Papaya',
                'value': 2,
                'amount': 1,
                'unit': Unit.KILOGRAM
            }, {
                'article_number': '004',
                'name': 'Lemon',
                'value': 5,
                'amount': 1,
                'unit': Unit.KILOGRAM
            },
            {
                'article_number': '005',
                'name': 'Salt',
                'value': 1,
                'amount': 500,
                'unit': Unit.GRAM
            }, {
                'article_number': '006',
                'name': 'Yogurt',
                'value': 2,
                'amount': 1,
                'unit': Unit.LITER
            }, {
                'article_number': '007',
                'name': 'Orange Juice',
                'value': 2,
                'amount': 1,
                'unit': Unit.LITER
            }, {
                'article_number': '008',
                'name': 'Milk',
                'value': 1,
                'amount': 1,
                'unit': Unit.LITER
            },
            {
                'article_number': '009',
                'name': 'Cream',
                'value': 200,
                'amount': 1,
                'unit': Unit.GRAM
            },
            {
                'article_number': '010',
                'name': 'Sugar',
                'value': 2,
                'amount': 500,
                'unit': Unit.GRAM
            },

        ]

        try:
            user = CustomUser.objects.first()

            for ingredient in ingredients:
                try:
                    ing = Ingredient.objects.create(
                        name=ingredient['name'],
                        article_number=ingredient['article_number'],
                        value=ingredient['value'],
                        amount=ingredient['amount'],
                        unit=Unit.objects.get(id=ingredient['unit']),
                        created_by=user
                    )
                    print('Ingredient created: {}'.format(ing))

                except IntegrityError:
                    pass

        except CustomUser.DoesNotExist:
            pass




