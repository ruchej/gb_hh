from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, TemplateView
from notifications.signals import notify

from . import models
from accounts.models import JobSeeker, Employer, UserStatus
from resumes.models import Resume
from vacancies.models import Vacancy

NEW_RESUME_NOTIF = 'New resume'


class ResponseListView(LoginRequiredMixin, ListView):
    """View for getting list of responses for job."""

    model = models.Response
    extra_context = {'title': 'Отклики'}
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ResponseListView, self).get_context_data(object_list=object_list, **kwargs)
        jobseekers = []
        new_resumes = []
        for notif in self.request.user.notifications.unread():
            if notif.verb == NEW_RESUME_NOTIF:
                new_resumes.append(notif.target)
        is_new = []
        for response in context['response_list']:
            is_new.append(True if response.resume in new_resumes else False)
            jobseekers.append(JobSeeker.objects.get(user=response.resume.user))
        context['jobseekers_resp_list'] = list(zip(jobseekers, context['response_list'], is_new))
        return context

    def get_queryset(self):
        return super().get_queryset().filter(vacancy__employer=self.request.user)

    def render_to_response(self, context, **response_kwargs):
        if self.request.user.status == UserStatus.JOBSEEKER:
            return redirect('blog:news')
        return super(ResponseListView, self).render_to_response(context, **response_kwargs)


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
