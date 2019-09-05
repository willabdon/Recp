from django.contrib import admin

from manager.models import Ingredient, Recipe, IngredientAmount


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('article_number', 'name')
    exclude = ('created', 'modified')


admin.site.register(Ingredient, IngredientAdmin)


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', )

    inlines = (IngredientAmountInline, )


admin.site.register(Recipe, RecipeAdmin)