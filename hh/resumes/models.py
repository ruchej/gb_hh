from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


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
    title = models.CharField(verbose_name=_('название должности'), max_length=64, db_index=True)
    salary = models.PositiveIntegerField(verbose_name=_('зарплата'), default=0, db_index=True)
    employment = models.CharField(verbose_name=_('занятость'), max_length=10)
    schedule = models.CharField(verbose_name=_('график работы'), max_length=10)
    relocation = models.CharField(verbose_name=_('переезд'), blank=True, max_length=4, choices=RELOCATION_CHOICES)
    business_trip = models.CharField(verbose_name=_('командировки'), blank=True, max_length=3, choices=TRIP_CHOICES)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = _('требования к должности')
        verbose_name_plural = _('требования к должностям')


class Experience(models.Model):
    """Model for keeping info about employee's experience."""

    skills = models.TextField(verbose_name=_('ключевые навыки'), blank=True, db_index=True)
    about = models.TextField(verbose_name=_('о себе'), db_index=True)
    portfolio = models.URLField(verbose_name=_('ссылка на портфолио'), blank=True)

    def __str__(self):
        return self.about

    class Meta:
        ordering = ('about',)
        verbose_name = _('опыт работы')
        verbose_name_plural = _('опыт работ')


class Job(models.Model):
    """Model for keeping info about jobs."""

    experience = models.ForeignKey(Experience, verbose_name=_('анкета "опыт работы"'), on_delete=models.CASCADE,
                                   db_index=True)
    # TODO: Connect database of ЕГРЮЛ to field 'organization'.
    organization = models.CharField(verbose_name=_('организация'), max_length=128)
    start = models.DateField(verbose_name=_('начало работы'))
    end = models.DateField(verbose_name=_('окончание работы'))
    # TODO: Connect database of regions to field 'location'.
    location = models.CharField(verbose_name=_('регион'), max_length=64)
    site = models.URLField(verbose_name=_('сайт'), blank=True)
    scope = models.CharField(verbose_name=_('сфера деятельности компании'), max_length=64)
    position = models.CharField(verbose_name=_('должность'), max_length=64, db_index=True)
    functions = models.TextField(verbose_name=_('обязанности на рабочем месте'), blank=True)

    def __str__(self):
        return self.organization

    class Meta:
        ordering = ('organization',)
        verbose_name = _('место работы')
        verbose_name_plural = _('места работ')


class Resume(models.Model):
    """Model for keeping employee's resume."""

    user = models.ForeignKey(User, verbose_name=_('пользователь'), on_delete=models.CASCADE, db_index=True)
    title = models.CharField(verbose_name=_('название'), max_length=128, db_index=True)
    photo = models.ImageField(verbose_name=_('фотография'), blank=True, upload_to='photos/')
    contacts = models.OneToOneField(Contacts, verbose_name=_('контакты'), on_delete=models.CASCADE)
    position = models.OneToOneField(Position, verbose_name=_('должность/зарплата'), on_delete=models.CASCADE,
                                    db_index=True)
    experience = models.OneToOneField(Experience, verbose_name=_('опыт работы'), on_delete=models.CASCADE,
                                      db_index=True)
    favourites = models.ManyToManyField(User, related_name='favourites_resumes', blank=True, default=None)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = _('резюме')
        verbose_name_plural = _('резюме')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.photo and self.user and self.user.avatar:
            self.photo = self.user.avatar
            self.save()
