from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import VacancyForm
from .models import Vacancy
from accounts.models import UserStatus


class VacancyList(LoginRequiredMixin, ListView):
    template_name = '../templates/vacancy-list.html'
    model = Vacancy
    paginate_by = 10
    filterset_class = None

    def get_context_data(self, **kwargs):
        context = super(VacancyList, self).get_context_data()
        context.update({'title': 'Вакансии'})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.status == UserStatus.EMPLOYER:
            queryset = queryset.filter(employer=self.request.user)
        return queryset


class VacancyDetail(LoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = 'vacancy-detail.html'
    extra_context = {'title': 'Детали Вакансии'}


class VacancyCreate(LoginRequiredMixin, CreateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = 'vacancy-create.html'
    extra_context = {'title': 'Создание Вакансии'}
    success_url = reverse_lazy('vacancies:vacancy_list')

    def form_valid(self, form):
        form.instance.employer_id = self.kwargs.get('pk')
        return super(VacancyCreate, self).form_valid(form)


class VacancyUpdate(LoginRequiredMixin, UpdateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = 'vacancy-update.html'
    extra_context = {'title': 'Изменение Вакансии'}
    success_url = reverse_lazy('vacancies:vacancy_list')


class VacancyDelete(LoginRequiredMixin, DeleteView):
    model = Vacancy
    template_name = 'vacancy-delete.html'
    extra_context = {'title': 'Удаление Вакансии'}
    success_url = reverse_lazy('vacancies:vacancy_list')
