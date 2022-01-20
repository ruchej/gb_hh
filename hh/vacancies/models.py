from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Vacancy(models.Model):
    """Модель вакансий от работодателя"""

    DRAFT = 'DF'
    WAITING = 'WTG'
    PUBLISHED = 'PBL'
    ARCHIVED = 'ARC'

    VACANCY_STATUS_CHOICES = (
        (DRAFT, _('Черновик')),
        (WAITING, _('Ожидает проверки')),
        (PUBLISHED, _('Опубликовано')),
        (ARCHIVED, _('Архивировано'))
    )

    FULL_TIME = 'FT'
    PART_TIME = 'PT'
    INTERNSHIP = 'INT'

    EMPLOYMENT_TYPE_CHOICES = (
        (FULL_TIME, _('Полная занятость')),
        (PART_TIME, _('Неполная занятость')),
        (INTERNSHIP, _('Стажировка'))
    )

    NO_EXP = 'NE'
    ONE_TO_THREE = 'OT'
    THREE_TO_SIX = 'TS'
    GREATER_SIX = 'GS'

    EXPERIENCE_CHOICES = (
        (NO_EXP, _('Без опыта')),
        (ONE_TO_THREE, _('От 1 до 3 лет')),
        (THREE_TO_SIX, _('От 3 до 6 лет')),
        (GREATER_SIX, _('Более 6 лет'))
    )

    employer = models.ForeignKey(
        User,
        verbose_name=_('Работодатель'),
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=50,
        verbose_name=_('Название')
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Описание')
    )
    hashtags = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('Ключевые навыки')
    )
    employment_type = models.CharField(
        choices=EMPLOYMENT_TYPE_CHOICES,
        max_length=3,
        verbose_name=_('Тип занятости')
    )
    experience = models.CharField(
        choices=EXPERIENCE_CHOICES,
        max_length=2,
        verbose_name=_('Опыт работы')
    )
    salary = models.CharField(
        max_length=30,
        default=_('Не указана'),
        verbose_name=_('Зарплата')
    )
    status = models.CharField(
        choices=VACANCY_STATUS_CHOICES,
        max_length=3,
        default=DRAFT,
        verbose_name=_('Статус')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Вакансия')
        verbose_name_plural = _('Вакансии')

    def delete(self, using=None, keep_parents=False):
        """Метод удаления вакансии"""
        self.status = self.ARCHIVED
        self.save()

    def __str__(self):
        # TODO: return employer and title
        return self.title
