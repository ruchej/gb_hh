from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Vacancy


class VacancyList(LoginRequiredMixin, ListView):
    template_name = '../templates/vacancy-list.html'
    model = Vacancy

    def get_context_data(self, **kwargs):
        context = super(VacancyList, self).get_context_data()
        context.update({'title': 'Вакансии'})
        return context
