from django.db import models


class Vacancy(models.Model):
    DRAFT = 'DF'
    WAITING = 'WTG'
    PUBLISHED = 'PBL'
    ARCHIVED = 'ARC'

    VACANCY_STATUS_CHOICES = (
        (DRAFT, 'Черновик'),
        (WAITING, 'Ожидает проверки'),
        (PUBLISHED, 'Опубликовано'),
        (ARCHIVED, 'Архивировано')
    )

    FULL_TIME = 'FT'
    PART_TIME = 'PT'
    INTERNSHIP = 'INT'

    EMPLOYMENT_TYPE_CHOICES = (
        (FULL_TIME, 'Полная занятость'),
        (PART_TIME, 'Неполная занятость'),
        (INTERNSHIP, 'Стажировка')
    )

    NO_EXP = 'NE'
    ONE_TO_THREE = 'OT'
    THREE_TO_SIX = 'TS'
    GREATER_SIX = 'GS'

    EXPERIENCE_CHOICES = (
        (NO_EXP, 'Без опыта'),
        (ONE_TO_THREE, 'От 1 до 3 лет'),
        (THREE_TO_SIX, 'От 3 до 6 лет'),
        (GREATER_SIX, 'Более 6 лет')
    )

    # TODO: add employer
    # employer = models.OneToOneField(
    #     Employer,
    #     on_delete=models.CASCADE
    # )
    employer = models.CharField(max_length=100)
    title = models.CharField(
        max_length=50,
        verbose_name='Название'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    hashtags = models.CharField(
        max_length=50,
        verbose_name='Ключевые навыки'
    )
    employment_type = models.CharField(
        choices=EMPLOYMENT_TYPE_CHOICES,
        max_length=3,
        verbose_name='Тип занятости'
    )
    experience = models.CharField(
        choices=EXPERIENCE_CHOICES,
        max_length=2,
        verbose_name='Опыт работы'
    )
    salary = models.CharField(
        max_length=30,
        default='Не указана',
        verbose_name='Зарплата'
    )
    status = models.CharField(
        choices=VACANCY_STATUS_CHOICES,
        max_length=3,
        default=DRAFT,
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def delete(self, using=None, keep_parents=False):
        """Метод удаления вакансии"""
        self.status = self.ARCHIVED
        self.save()

    def __str__(self):
        # TODO: return employer and title
        return self.title
