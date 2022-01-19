from django.db import models
from django.utils.translation import gettext_lazy as _

from resumes import models as resumes_models
from vacancies import models as vacancies_models


class Response(models.Model):
    """Model for keeping response from employee for job."""

    resume = models.ForeignKey(resumes_models.Resume, verbose_name=_('резюме'), on_delete=models.CASCADE)
    vacancy = models.ForeignKey(vacancies_models.Vacancy, verbose_name=_('вакансия'), on_delete=models.CASCADE)


class Offer(models.Model):
    """Model for keeping offer from employer to employee."""

    vacancy = models.ForeignKey(vacancies_models.Vacancy, verbose_name=_('вакансия'), on_delete=models.CASCADE)
    resume = models.ForeignKey(resumes_models.Resume, verbose_name=_('резюме'), on_delete=models.CASCADE)
