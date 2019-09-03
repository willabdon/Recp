from django.http import HttpResponseBadRequest


def calc_total_ingredient(ingredient_amount):
    total_amount = ingredient_amount.ingredient.amount
    price = ingredient_amount.ingredient.value

    def calc_total(amount):
        return (price * amount) / total_amount

    if ingredient_amount.unit == ingredient_amount.ingredient.unit:
        total = calc_total(ingredient_amount.amount)
    else:
        convert = getattr(ingredient_amount.ingredient.unit,
                          '{}_to_{}'.format(ingredient_amount.unit, ingredient_amount.ingredient.unit))
        converted_amount = convert(ingredient_amount.amount)
        total = calc_total(converted_amount)

    return total


def get_choices(choices):
    initial = ('', '-------')
    return [initial] + [(x.id, x) for x in choices]
