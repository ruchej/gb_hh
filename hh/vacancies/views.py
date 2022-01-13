from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Vacancy


class VacancyList(LoginRequiredMixin, ListView):
    template_name = '../templates/vacancy-list.html'
    model = Vacancy
