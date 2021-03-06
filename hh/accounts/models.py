from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from cities_light.models import Country, City

from conf.choices import SexChoices, UserStatusChoices, PublicStatusChoices


class AccountManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class JobSeekerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user__status=UserStatusChoices.JOBSEEKER)


class EmployerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(user__status=UserStatusChoices.EMPLOYER)


class Account(AbstractUser):
    status = models.PositiveSmallIntegerField(
        choices=UserStatusChoices.choices,
        default=UserStatusChoices.JOBSEEKER,
        verbose_name=_("Статус пользователя"),
        db_index=True
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
        from chat.models import Contact
        if not Contact.objects.filter(user=self).exists():
            contact = Contact(user=self)
            contact.save()
        if self.status == UserStatusChoices.EMPLOYER:
            if not Employer.objects.filter(user=self).exists():
                employer = Employer(user=self)
                employer.save()
        elif self.status == UserStatusChoices.JOBSEEKER:
            if not JobSeeker.objects.filter(user=self).exists():
                seeker = JobSeeker(user=self)
                seeker.save()


class JobSeeker(models.Model):
    """Соискатель"""

    user = models.OneToOneField(
        Account, related_name="seeker", on_delete=models.PROTECT, verbose_name=_('Пользователь'),
        db_index=True)
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name=_('Имя'),
        db_index=True)
    patronymic = models.CharField(
        max_length=20, blank=True, default="", verbose_name=_("Отчество")
    )
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name=_('Фамилия'),
        db_index=True)
    date_birth = models.DateField(
        blank=True, null=True, verbose_name=_("Дата рождения"))
    sex = models.BooleanField(
        choices=SexChoices.choices, null=True, blank=True, verbose_name=_("Пол"))
    phone = models.CharField(max_length=20, blank=True,
                             verbose_name=_("Телефон"))
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True,
                                verbose_name=_("страна проживания"))
    city = models.ForeignKey(City, on_delete=models.PROTECT, db_index=True,
                             null=True, blank=True, verbose_name=_("город проживания"))
    address = models.TextField(blank=True, verbose_name=_("адрес"))
    objects = JobSeekerManager()

    class Meta:
        verbose_name = _("соискателя")
        verbose_name_plural = _("Соискатели")

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        name = full_name if full_name else str(self.user)
        return name


class Employer(models.Model):
    """Работодатель"""

    user = models.OneToOneField(
        Account, related_name="employer", on_delete=models.CASCADE, verbose_name=_("Работодатель")
    )
    name = models.CharField(
        blank=True, null=True, max_length=500, verbose_name=_("название компании"),
        db_index=True)
    description = models.TextField(
        blank=True, null=True, verbose_name=_("Описание"))
    phone = models.CharField(max_length=20, blank=True,
                             verbose_name=_("телефон"))
    country = models.ForeignKey(Country, on_delete=models.PROTECT, null=True, blank=True,
                                verbose_name=_("страна"))
    city = models.ForeignKey(City, on_delete=models.PROTECT, db_index=True,
                             null=True, blank=True, verbose_name=_("город"))
    address = models.TextField(blank=True, verbose_name=_("штаб квартира"))
    objects = EmployerManager()

    class Meta:
        verbose_name = _("работодателя")
        verbose_name_plural = _("Работодатели")

    def __str__(self):
        return self.name if self.name else str(self.user)

    def vacancy_amount(self):
        from vacancies.models import Vacancy
        return Vacancy.objects.filter(employer=self.user, status=PublicStatusChoices.PUBLISHED).count()
