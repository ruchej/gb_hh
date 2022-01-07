from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _


class UserStatus(models.IntegerChoices):
    MODERATOR = 0, _("Модератор")
    JOBSEEKER = 1, _("Соискатель")
    EMPLOYER = 2, _("Работодатель")


class AccountManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class JobSeekerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(status=UserStatus.JOBSEEKER)


class EmployerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(status=UserStatus.EMPLOYER)


class Account(AbstractUser):
    patronymic = models.CharField(
        max_length=20, blank=True, default="", verbose_name=_("Отчество")
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Телефон"))
    adress = models.TextField(blank=True, verbose_name=_("Район поиска"))
    status = models.PositiveSmallIntegerField(
        choices=UserStatus.choices,
        default=UserStatus.JOBSEEKER,
        verbose_name=_("Статус пользователя"),
    )
    objects = AccountManager()
    seeker = JobSeekerManager()
    employer = EmployerManager()

    class Meta:

        verbose_name = _("пользователя")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return f"{self.first_name} {self.patronymic} {self.last_name}"
