from django.db import models
from django.utils.translation import gettext_lazy as _


class PersonalInfo(models.Model):
    """Model for keeping personal info of employee."""

    GENDER_CHOICES = (
        ('ML', _('мужской')),
        ('FML', _('женский')),
        ('OTH', _('другой')),
    )
    RELOCATION_CHOICES = (
        ('NOT', _('невозможен')),
        ('RDY', _('возможен')),
        ('WISH', _('желателен')),
    )
    TRIP_CHOICES = (
        ('NOT', _('никогда')),
        ('RDY', _('готов')),
        ('SMT', _('иногда')),
    )
    name = models.CharField(verbose_name=_('имя'), max_length=32)
    patronymic = models.CharField(verbose_name=_('отчество'), blank=True, max_length=32)
    surname = models.CharField(verbose_name=_('фамилия'), max_length=32)
    birthday = models.DateField(verbose_name=_('дата рождения'), blank=True)
    gender = models.CharField(verbose_name=_('пол'), blank=True, max_length=3, choices=GENDER_CHOICES)
    # TODO: Connect cities database to fields 'location', 'relocation'.
    location = models.CharField(verbose_name=_('город проживания'), blank=True, max_length=32)
    relocation = models.CharField(verbose_name=_('переезд'), blank=True, max_length=4, choices=RELOCATION_CHOICES)
    business_trip = models.CharField(verbose_name=_('командировки'), blank=True, max_length=3, choices=TRIP_CHOICES)

    def display_full_name(self):
        """Return employee's full name."""

        return f'{self.surname} {self.name} {self.patronymic}' if self.patronymic else f'{self.surname} {self.name}'

    def __str__(self):
        return self.display_full_name()

    class Meta:
        ordering = ('surname',)
        verbose_name = _('персональная информация')
        verbose_name_plural = _('персональная информация')


class Contacts(models.Model):
    """Model for keeping contacts of employee."""

    # TODO: Add phones database to field 'phone'.
    phone = models.CharField(verbose_name=_('мобильный телефон'), blank=True, max_length=20)
    email = models.EmailField(verbose_name=_('электронная почта'), max_length=254)
    telegram = models.CharField(verbose_name=_('аккаунт в "Telegram"'), blank=True, max_length=64)

    def __str__(self):
        return f'{self.email} | {self.phone} | {self.telegram}'

    class Meta:
        ordering = ('email',)
        verbose_name = _('контакты')
        verbose_name_plural = _('контакты')


class Position(models.Model):
    """Model for keeping info about wishing position."""

    title = models.CharField(verbose_name=_('название должности'), max_length=64)
    salary = models.PositiveIntegerField(verbose_name=_('зарплата'), default=0)
    employment = models.CharField(verbose_name=_('занятость'), max_length=10)
    schedule = models.CharField(verbose_name=_('график работы'), max_length=10)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = _('требования к должности')
        verbose_name_plural = _('требования к должностям')


class Experience(models.Model):
    """Model for keeping info about employee's experience."""

    skills = models.TextField(verbose_name=_('ключевые навыки'), blank=True)
    about = models.TextField(verbose_name=_('о себе'))
    portfolio = models.URLField(verbose_name=_('ссылка на портфолио'), blank=True)

    def __str__(self):
        return self.about

    class Meta:
        ordering = ('about',)
        verbose_name = _('опыт работы')
        verbose_name_plural = _('опыт работ')


class Job(models.Model):
    """Model for keeping info about jobs."""

    experience = models.ForeignKey(Experience, verbose_name=_('анкета "опыт работы"'), on_delete=models.CASCADE)
    # TODO: Connect database of ЕГРЮЛ to field 'organization'.
    organization = models.CharField(verbose_name=_('организация'), max_length=128)
    start = models.DateField(verbose_name=_('начало работы'))
    end = models.DateField(verbose_name=_('окончание работы'))
    # TODO: Connect database of regions to field 'location'.
    location = models.CharField(verbose_name=_('регион'), max_length=64)
    site = models.URLField(verbose_name=_('сайт'), blank=True)
    scope = models.CharField(verbose_name=_('сфера деятельности компании'), max_length=64)
    position = models.CharField(verbose_name=_('должность'), max_length=64)
    functions = models.TextField(verbose_name=_('обязанности на рабочем месте'), blank=True)

    def __str__(self):
        return self.organization

    class Meta:
        ordering = ('organization',)
        verbose_name = _('место работы')
        verbose_name_plural = _('места работ')


class Resume(models.Model):
    """Model for keeping employee's resume."""

    # TODO: Add link to employee (fk).
    title = models.CharField(verbose_name=_('название'), max_length=128)
    photo = models.ImageField(verbose_name=_('фотография'), blank=True, upload_to='photos/')
    personal_info = models.OneToOneField(PersonalInfo, verbose_name=_('личная информация'), on_delete=models.CASCADE)
    contacts = models.OneToOneField(Contacts, verbose_name=_('контакты'), on_delete=models.CASCADE)
    position = models.OneToOneField(Position, verbose_name=_('должность/зарплата'), on_delete=models.CASCADE)
    experience = models.OneToOneField(Experience, verbose_name=_('опыт работы'), on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = _('резюме')
        verbose_name_plural = _('резюме')
