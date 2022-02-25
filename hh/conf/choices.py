"""
Все чойсы решено перенести отдельно для более удобного доступа
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserStatusChoices(models.IntegerChoices):
    MODERATOR = 0, _("Модератор")
    JOBSEEKER = 1, _("Соискатель")
    EMPLOYER = 2, _("Работодатель")


class RelocationChoices(models.IntegerChoices):
    IMPOSSIBLE = 0, _('невозможен')
    POSSIBLE = 1, _('возможен')
    DESIRABLE = 2, _('желателен')


class TripChoices(models.IntegerChoices):
    NEVER = 0, _('никогда')
    READY = 1, _('готов')
    SOMETIMES = 2, _('иногда')


class SexChoices(models.IntegerChoices):
    WOMAN = 0, "Женщина"
    MAN = 1, "Мужчина"
    __empty__ = _('не выбрано')


class PublicStatusChoices(models.IntegerChoices):
    DRAFT = 0, _('Черновик')
    WAITING = 1, _('Ожидает проверки')
    PUBLISHED = 2, _('Опубликовано')
    ARCHIVED = 3, _('Архивировано')


class EmploymentTypeChoices(models.IntegerChoices):
    FULL_TIME = 0, _('Полная занятость')
    PART_TIME = 1, _('Неполная занятость')
    INTERNSHIP = 2, _('Стажировка')


class ExperienceChoices(models.IntegerChoices):
    NO_EXP = 0, _('Без опыта')
    ONE_TO_THREE = 1, _('От 1 до 3 лет')
    THREE_TO_SIX = 2, _('От 3 до 6 лет')
    GREATER_SIX = 3, _('Более 6 лет')