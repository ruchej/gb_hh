from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import Account



class AccountChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Account


@admin.register(Account)
class AccountAdmin(UserAdmin):

    form = AccountChangeForm

    list_display = ('username', 'first_name', 'last_name', 'status')
    fieldsets = (
        (
            'Пользователь',
            {
                'fields': (
                    'username',
                    ('first_name', 'patronymic', 'last_name'),
                    'email',
                    'phone',
                    'adress',
                )
            },
        ),
        (
            'Статус',
            {
                'fields': (
                    'status',
                    'is_superuser',
                    'is_staff',
                    'is_active',
                    'date_joined',
                )
            },
        ),
        (
            'Прочее',
            {
                'fields': (
                    'groups',
                    'user_permissions',
                    'last_login',
                    'password',
                ),
                'classes': ('collapse', 'wide', 'extrapretty'),
            },
        ),
    )

