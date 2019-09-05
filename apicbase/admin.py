from django.contrib import admin
from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    fields = ('first_name', 'last_name', 'email', 'last_login', 'is_superuser', 'is_staff')
    readonly_fields = ('last_login', )


admin.site.register(CustomUser, UserAdmin)
