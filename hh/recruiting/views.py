from collections import Counter

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import ListView, CreateView, TemplateView
from notifications.signals import notify
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from . import models
from accounts.models import JobSeeker, Employer, UserStatus
from resumes.models import Resume
from vacancies.models import Vacancy
from el_pagination.views import AjaxListView

NEW_RESUME_NOTIF = 'New resume'


class ResponseListView(LoginRequiredMixin, AjaxListView):
    """View for getting list of responses for job."""

    model = models.Response
    page_template = 'recruiting/snippets/response/list/cards.html'
    TOTAL_K = _('Все')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ResponseListView, self).get_context_data(object_list=object_list, **kwargs)
        self.filter(context, object_list)
        context['title'] = 'Отклики'
        return context

    def get_queryset(self):
        return super().get_queryset().filter(vacancy__employer=self.request.user, accepted=False, rejected=False)

    def render_to_response(self, context, **response_kwargs):
        if self.request.user.status == UserStatus.JOBSEEKER:
            return redirect('blog:news')
        if self.request.is_ajax() and 'page' not in self.request.GET:
            result = render_to_string(self.page_template, context=context, request=self.request)
            return JsonResponse({'result': result})
        return super(ResponseListView, self).render_to_response(context, **response_kwargs)

    def filter(self, context, object_list):
        jobseekers, new_resumes, vacancies, is_new, cities = [], [], [], [], []
        for notif in self.request.user.notifications.unread():
            if notif.verb == NEW_RESUME_NOTIF:
                new_resumes.append(notif.target)
        vac_id = 0
        # Check if search by vacancy was invoked
        if 'vac_id' in self.request.GET and self.request.GET['vac_id']:
            vac_id = int(self.request.GET['vac_id'])
            responses = object_list.filter(vacancy__id=vac_id)
        else:
            responses = object_list

        # Check if search by city was invoked
        if 'city_id' in self.request.GET and self.request.GET['city_id']:
            city_id = int(self.request.GET['city_id'])
            jobseekers_cities = JobSeeker.objects.filter(city__id=city_id)
        else:
            jobseekers_cities = JobSeeker.objects.all()

        # Check if normal search was invoked
        if 'search' in self.request.GET and (text := self.request.GET['search']):
            jobseekers = jobseekers_cities.filter(
                Q(first_name__contains=text) |
                Q(last_name__contains=text)
            )
            if text.isnumeric():
                resumes = Resume.objects.filter(position__salary=int(text))
            else:
                resumes = Resume.objects.filter(
                    Q(experience__skills=text) |
                    Q(position__title=text) |
                    Q(position__employment=text) |
                    Q(position__schedule=text) |
                    Q(position__relocation=text) |
                    Q(position__business_trip=text)
                )
            if jobseekers:
                new_responses = []
                for jobseeker in jobseekers:
                    js_resumes = list(Resume.objects.filter(user=jobseeker.user))
                    for resume in js_resumes:
                        if js_responses := responses.filter(resume=resume):
                            new_responses.extend(list(js_responses))
                responses = new_responses
            elif resumes:
                new_responses = []
                for resume in resumes:
                    if (res_responses := responses.filter(resume=resume)) and \
                            jobseekers_cities.filter(user=resume.user).exists():
                        new_responses.extend(list(res_responses))
                responses = new_responses
            else:
                responses = []
        else:
            new_responses = []
            for jobseeker in jobseekers_cities:
                js_resumes = list(Resume.objects.filter(user=jobseeker.user))
                for resume in js_resumes:
                    if js_responses := responses.filter(resume=resume):
                        new_responses.extend(list(js_responses))
            responses = new_responses
        jobseekers = []

        for response in responses:
            is_new.append(True if response.resume in new_resumes else False)
            jobseeker = JobSeeker.objects.get(user=response.resume.user)
            jobseekers.append(jobseeker)
            cities.append(jobseeker.city)
            vacancies.append(response.vacancy)

        context['responses_vacancies'] = sorted(Counter(vacancies).items(), key=lambda x: x[1], reverse=True)[:4]
        context['responses_vacancies'].insert(0, (self.TOTAL_K, len(object_list)))

        context['responses_cities'] = sorted(Counter(cities).items(), key=lambda x: x[1], reverse=True)[:4]
        context['responses_cities'].insert(0, (self.TOTAL_K, len(object_list)))

        context['jobseekers_resp_list'] = list(zip(jobseekers, responses, is_new))

        return jobseekers, responses, is_new


class ResponseCreateView(LoginRequiredMixin, TemplateView):
    """View for creating response for job."""
    template_name = 'recruiting/response_create.html'
    model = models.Response

    def dispatch(self, request, *args, **kwargs):
        return super(ResponseCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ResponseCreateView, self).get_context_data(object_list=object_list, **kwargs)
        context['vacancy'] = Vacancy.objects.get(id=context['v_pk'])
        context['employer'] = Employer.objects.get(user=context['vacancy'].employer)
        context['resumes'] = Resume.objects.filter(user=self.request.user)
        context['title'] = f'Подача резюме в {context["employer"].name}'
        return context

    def render_to_response(self, context, **response_kwargs):
        if models.Response.objects.filter(resume__user=self.request.user, vacancy=context['vacancy']).exists():
            return redirect('vacancies:vacancy_list')
        if 'v_pk' in context and 'r_pk' in context:
            resume = Resume.objects.get(id=context['r_pk'])
            if not models.Response.objects.filter(resume=resume, vacancy=context['vacancy']).exists() and \
                    resume.user == self.request.user:
                notify.send(self.request.user, recipient=context['vacancy'].employer,
                            verb=NEW_RESUME_NOTIF, target=resume)
                models.Response.objects.create(resume=resume, vacancy=context['vacancy'])
            return redirect('vacancies:vacancy_list')
        return super(ResponseCreateView, self).render_to_response(context, **response_kwargs)


def response_accept(request, r_pk):
    response = models.Response.objects.get(id=r_pk)
    response.accepted = True
    response.rejected = False
    response.save()


def response_reject(request, r_pk):
    response = models.Response.objects.get(id=r_pk)
    response.accepted = False
    response.rejected = True
    response.save()


class ResponseDeleteView(LoginRequiredMixin, CreateView):
    """View for deleting response for job."""

    model = models.Response


class OfferListView(LoginRequiredMixin, ListView):
    """View for getting list of offers."""

    model = models.Offer


def offer_create(v_pk, r_pk=None):
    models.Offer.objects.create(resume__id=r_pk, vacancy__id=v_pk)


class OfferCreateView(LoginRequiredMixin, CreateView):
    """View for creating offer."""

    model = models.Offer


class OfferDeleteView(LoginRequiredMixin, CreateView):
    """View for deleting offer."""

    model = models.Offer


def get_notifications(request):
    from conf.context_processor import new_responses
    if request.is_ajax():
        return JsonResponse(new_responses(request))
