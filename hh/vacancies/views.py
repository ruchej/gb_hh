from django.views.generic import ListView

from .models import Vacancy


class VacancyList(ListView):
    template_name = '../templates/vacancy-list.html'
    model = Vacancy
