import re

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from conf.choices import EmploymentTypeChoices, ExperienceChoices, PublicStatusChoices

User = get_user_model()


class Vacancy(models.Model):
    """Модель вакансий от работодателя"""

    employer = models.ForeignKey(
        User,
        verbose_name=_('Работодатель'),
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=500,
        verbose_name=_('Название'),
        db_index=True
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Описание')
    )
    hashtags = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_('Ключевые навыки'),
        db_index=True
    )
    employment_type = models.SmallIntegerField(
        choices=EmploymentTypeChoices.choices,
        verbose_name=_('Тип занятости'),
        db_index=True,
        default=EmploymentTypeChoices.FULL_TIME
    )
    experience = models.SmallIntegerField(
        choices=ExperienceChoices.choices,
        verbose_name=_('Опыт работы'),
        db_index=True,
        default=ExperienceChoices.NO_EXP
    )
    salary = models.CharField(
        max_length=30,
        default=_('Не указана'),
        verbose_name=_('Зарплата'),
        db_index=True
    )
    status = models.SmallIntegerField(
        choices=PublicStatusChoices.choices,
        default=PublicStatusChoices.DRAFT,
        verbose_name=_('Статус')
    )
    modified_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now_add=True)
    favourites = models.ManyToManyField(User, related_name='favourites_vacancies', blank=True, default=None)

    class Meta:
        verbose_name = _('Вакансия')
        verbose_name_plural = _('Вакансии')

    def delete(self, using=None, keep_parents=False):
        """Метод удаления вакансии"""
        self.status = PublicStatusChoices.ARCHIVED
        self.save()

    def __str__(self):
        # TODO: return employer and title
        return self.title

    def hashtags_as_list(self):
        return re.split(r'[^a-zA-Z0-9а-яА-Я \+#\.\-—]', self.hashtags)[:5]
        # return self.hashtags.split(', ')[:5]
