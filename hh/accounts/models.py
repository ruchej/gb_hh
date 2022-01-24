from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
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
        return super().get_queryset().filter(user__status=UserStatus.JOBSEEKER)


class EmployerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user__status=UserStatus.EMPLOYER)


class Account(AbstractUser):

    status = models.PositiveSmallIntegerField(
        choices=UserStatus.choices,
        default=UserStatus.JOBSEEKER,
        verbose_name=_("Статус пользователя"),
    )
    avatar = models.ImageField(
        upload_to="avatars", blank=True, null=True, verbose_name=_("аватар"))
    objects = AccountManager()
    seeker = JobSeekerManager()
    employer = EmployerManager()

    first_name = None
    last_name = None
    """
    email
    is_staff
    is_active
    date_joined
    """
    class Meta:

        verbose_name = _("пользователя")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return self.username

    def delete(self, **kwargs):
        if 'force' in kwargs:
            super().delete()
        else:
            self.is_active = False
            self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == UserStatus.EMPLOYER:
            if not Employer.objects.filter(user=self).exists():
                employer = Employer(user=self)
                employer.save()
        elif self.status == UserStatus.JOBSEEKER:
            if not JobSeeker.objects.filter(user=self).exists():
                seeker = JobSeeker(user=self)
                seeker.save()


class JobSeeker(models.Model):
    """Соискатель"""

    class Sex(models.IntegerChoices):
        WOMAN = 0, "Женщина"
        MAN = 1, "Мужчина"

    user = models.OneToOneField(
        Account, related_name="seeker", on_delete=models.PROTECT, verbose_name=_('Пользователь'))
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name=_('Имя'))
    patronymic = models.CharField(
        max_length=20, blank=True, default="", verbose_name=_("Отчество")
    )
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name=_('Фамилия'))
    date_birth = models.DateField(
        blank=True, null=True, verbose_name=_("Дата рождения"))
    sex = models.BooleanField(
        choices=Sex.choices, null=True, blank=True, verbose_name=_("Пол"))
    phone = models.CharField(max_length=20, blank=True,
                             verbose_name=_("Телефон"))
    adress = models.TextField(blank=True, verbose_name=_("Район поиска"))
    objects = JobSeekerManager()

    class Meta:

        verbose_name = _("сосискателя")
        verbose_name_plural = _("Соискатели")

    def __str__(self):
        full_name = f"{self.first_name} {self.patronymic} {self.last_name}".strip()
        name = full_name if full_name else str(self.user)
        return name


class Employer(models.Model):
    """Работодатель"""

    user = models.OneToOneField(
        Account, related_name="employer", on_delete=models.PROTECT, verbose_name=_("Работодатель")
    )
    description = models.TextField(
        blank=True, null=True, verbose_name=_("Описание"))
    objects = EmployerManager()

    class Meta:
        verbose_name = _("работодателя")
        verbose_name_plural = _("Работодатели")

    def __str__(self):
        return str(self.user)
