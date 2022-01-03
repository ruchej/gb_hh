from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.enums import Choices


class ExperienceYear(models.IntegerChoices):
    """Перечисления опыта работы в годах для требования вакансий"""

    NO_EXPERIENCE = 0, "Нет опыта"
    ONE_TO_THREE = 1, "От 1 до 3 лет"
    THREE_TO_SIX = 2, "От 3 до 6 лет"
    MORE_SIX = 3, "Более 6 лет"


class User(AbstractUser):
    class Status(models.IntegerChoices):
        MODERATOR = 0, "Модератор"
        JOBSEEKER = 1, "Соискатель"
        EMPLOYER = 2, "Работодатель"

    patronymic = models.CharField(
        max_length=20, blank=True, default="", verbose_name="Отчество"
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    adress = models.TextField(blank=True, verbose_name="Район поиска")
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.JOBSEEKER,
        verbose_name="Статус пользователя",
    )

    class Meta:

        verbose_name = "пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.first_name} {self.patronymic} {self.last_name}"


class JobSeeker(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, verbose_name="Соискатель"
    )

    class Meta:
        verbose_name = "соискателя"
        verbose_name_plural = "Соискатели"

    def __str__(self):
        return self.user


class Employer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, verbose_name="Работодатель"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "работодателя"
        verbose_name_plural = "Работодатели"

    def __str__(self):
        return self.user


class Resume(models.Model):
    class Sex(models.IntegerChoices):
        WOMAN = 0, "Женщина"
        MAN = 1, "Мужчина"

    class Move(models.IntegerChoices):
        IMPOSSIBLE = 0, "Не возможен"
        POSSIBLE = 1, "Возможен"
        DESIRABLE = 2, "Желателен"

    jobseeker = models.OneToOneField(
        JobSeeker, blank=False, on_delete=models.PROTECT, verbose_name="Соискатель"
    )
    title = models.CharField(max_length=200, verbose_name="Название")
    date_birth = models.DateField(verbose_name="Дата рождения")
    sex = models.BooleanField(choices=Sex.choices, verbose_name="Пол")
    city_residence = models.ForeignKey(
        "City", on_delete=models.PROTECT, verbose_name="Город проживания"
    )
    moving = models.SmallIntegerField(
        choices=Move.choices, default=Move.IMPOSSIBLE, verbose_name="Переезд"
    )
    position = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Желаемая должность"
    )
    salary = models.DecimalField(
        max_digits=7, decimal_places=0, default=0, verbose_name="Желаемая оплата"
    )
    employment = models.ManyToManyField("Employment", verbose_name="Занятость")
    experience = models.ManyToManyField("WorkExperience", verbose_name="Опыт работы")
    about = models.TextField(blank=True, null=True, verbose_name="Обо мне")

    class Meta:
        verbose_name = "резюме"
        verbose_name_plural = "Резюме"

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLIC = 1, "Опубликовано"
        ARCHIV = 2, "Архив"

    employer = models.OneToOneField(
        Employer, on_delete=models.PROTECT, verbose_name="Работодатель"
    )
    title = models.CharField(max_length=200, verbose_name="Название")
    experience = models.SmallIntegerField(
        choices=ExperienceYear.choices,
        default=ExperienceYear.NO_EXPERIENCE,
        on_delete=models.PROTECT,
        verbose_name="Опыт работы",
    )
    employment_type = models.ManyToManyField(
        "EmploymentType", verbose_name="Тип занятости"
    )
    working_schedule = models.ManyToManyField(
        "WorkingSchedule", verbose_name="График работы"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    duty = models.TextField(blank=True, null=True, verbose_name="Обязаности")
    requirements = models.TextField(blank=True, null=True, verbose_name="Требования")
    conditions = models.TextField(blank=True, null=True, verbose_name="Условия")
    date_publication = models.DateField(
        auto_now_add=True, verbose_name="Дата публикации"
    )
    status = models.SmallIntegerField(
        choices=Status.choices, default=Status.DRAFT, verbose_name="Статус"
    )

    class Meta:
        verbose_name = "вакансию"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.title


class WorkExperience(models.Model):
    """Опыт работы соискателя"""

    date_begin = models.DateField(verbose_name="Начало работы")
    date_end = models.DateField(blank=True, null=True, verbose_name="Окончание работы")
    till_present = models.BooleanField(verbose_name="По настоящее время")
    organization = models.CharField(max_length=255, verbose_name="Организация")
    region = models.ForeignKey("City", on_delete=models.PROTECT, verbose_name="Регион")
    scope = models.TextField(verbose_name="Сфера деятельности ккомпании")
    position = models.CharField(max_length=100, verbose_name="Должность")
    duties = models.TextField(verbose_name="Обязаности на рабочем месте")

    class Meta:
        verbose_name = "место работы"
        verbose_name_plural = "Места работ"

    def __str__(self):
        return self.organization
