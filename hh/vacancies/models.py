from django.db import models


class Position(models.Model):
    SW_DEVELOPER = 'SW_DEV'
    ELECTRICAL_ENG = 'E_ENG'
    MECHANICAL_ENG = 'M_ENG'

    POSITION_CHOICES = (
        (SW_DEVELOPER, 'Разработчик ПО'),
        (ELECTRICAL_ENG, 'Инженер-электрик'),
        (MECHANICAL_ENG, 'Инженер-механик')
    )

    title = models.CharField(
        choices=POSITION_CHOICES,
        max_length=50,
        verbose_name='Должность'
    )


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

    # TODO: add employer
    # employer = models.OneToOneField(
    #     Employer,
    #     on_delete=models.CASCADE
    # )
    employer = models.CharField(max_length=100)
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    positions = models.ManyToManyField(
        Position,
        verbose_name='Должности'
    )
    employment_type = models.CharField(
        choices=EMPLOYMENT_TYPE_CHOICES,
        max_length=30,
        verbose_name='Тип занятости'
    )
    # TODO: experience choices
    # experience = models.CharField(
    #     choices=EXPERIENCE_CHOICES,
    #     verbose_name='Опыт работы'
    # )
    status = models.CharField(
        choices=VACANCY_STATUS_CHOICES,
        max_length=30,
        default=DRAFT,
        verbose_name='Статус'
    )
    num_of_applications = models.PositiveIntegerField(
        default=0,
        verbose_name='Подано резюме'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField()

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
