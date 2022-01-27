from curses.ascii import EM
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import Account, JobSeeker, Employer


class AccountChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Account


@admin.register(Account)
class AccountAdmin(UserAdmin):

    form = AccountChangeForm

    list_display = ("username", "status")
    fieldsets = (
        (
            "Пользователь",
            {
                "fields": (
                    "username",
                    "email",
                )
            },
        ),
        (
            "Статус",
            {
                "fields": (
                    "status",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "date_joined",
                )
            },
        ),
        (
            "Прочее",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                    "last_login",
                    "password",
                ),
                "classes": ("collapse", "wide", "extrapretty"),
            },
        ),
    )

@admin.register(JobSeeker)
class JobSeekrAdmin(admin.ModelAdmin):
    pass


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    pass