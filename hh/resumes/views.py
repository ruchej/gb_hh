from collections import Counter

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from el_pagination.views import AjaxListView
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.forms.models import model_to_dict

from accounts.views import UserNotAuthMixin
from . import models, forms
from accounts.models import JobSeeker
from conf.choices import UserStatusChoices
from recruiting.views import NEW_RESUME_NOTIF
from .forms import ResumeForm
from .models import Resume


def resume_favorite_list(request):
    user = request.user
    favorites_resumes = user.favourites_resumes.all()
    jobseekers, favs = [], []
    for resume in favorites_resumes:
        jobseekers.append(JobSeeker.objects.get(user=resume.user))
        favs.append(True)
    context = {
        'favorites_resumes': zip(favorites_resumes, jobseekers, favs),
    }
    return render(request, 'resumes/favorites_resume_list.html', context)


class ResumeListView(LoginRequiredMixin, AjaxListView):
    """View for getting list of all resumes."""

    model = models.Resume
    page_template = 'resumes/snippets/list/resume_card.html'
    TOTAL_K = _('Все')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ResumeListView, self).get_context_data(object_list=object_list, **kwargs)
        context.update({'title': 'Мои Резюме'})
        if self.request.user.status == UserStatusChoices.JOBSEEKER:
            context['object_list'] = self.employee_filter(context, object_list)
            context['jobseeker'] = JobSeeker.objects.get(user=self.request.user)
            context['jobs'] = models.Job.objects.filter(user=self.request.user).order_by('-start')
        else:
            context['title'] = 'Резюме Соискателей'
            resumes, jobseekers, context['resumes_cities'] = self.employer_filter(context, object_list)
            favs = [True if self.request.user in resume.favourites.all() else False for resume in resumes]
            context['jobseekers_resume_list'] = list(zip(jobseekers, resumes, favs))
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.status == UserStatusChoices.JOBSEEKER:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax() and 'page' not in self.request.GET:
            result = render_to_string(self.page_template, context=context, request=self.request)
            return JsonResponse({'result': result})
        return super(ResumeListView, self).render_to_response(context, **response_kwargs)

    def employee_filter(self, context, object_list):
        if 'search' in self.request.GET and (text := self.request.GET['search']):
            if text.isnumeric():
                object_list = object_list.filter(position__salary=int(text))
            else:
                object_list = object_list.filter(
                    Q(title__contains=text) |
                    Q(experience__skills__contains=text) |
                    Q(experience__about__contains=text) |
                    Q(position__title__contains=text) |
                    Q(position__employment__contains=text) |
                    Q(position__schedule__contains=text) |
                    Q(position__relocation__contains=text) |
                    Q(position__business_trip__contains=text)
                )
        return object_list

    def employer_filter(self, context, object_list):
        response_resumes_ids = [res.id for res in object_list
                                if (self.request.user in res.accepted_by.all() or
                                    self.request.user in res.rejected_by.all())]
        # responses = Response.objects.filter(vacancy__employer=self.request.user).select_related('resume')
        # response_resumes_ids = [resp.resume.id for resp in responses]
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
                resumes = object_list.exclude(id__in=response_resumes_ids).filter(position__salary=int(text))
            else:
                resumes = object_list.exclude(id__in=response_resumes_ids).filter(
                    Q(experience__skills=text) |
                    Q(position__title=text) |
                    Q(position__employment=text) |
                    Q(position__schedule=text) |
                    Q(position__relocation=text) |
                    Q(position__business_trip=text)
                )
            if jobseekers:
                new_resumes = []
                for jobseeker in jobseekers:
                    js_resumes = list(object_list.exclude(id__in=response_resumes_ids).filter(user=jobseeker.user))
                    new_resumes.extend(js_resumes)
                resumes = new_resumes
            elif resumes:
                new_resumes = []
                for resume in resumes:
                    if jobseekers_cities.filter(user=resume.user).exists():
                        new_resumes.extend(resume)
                resumes = new_resumes
            else:
                resumes = []
        else:
            new_resumes = []
            for jobseeker in jobseekers_cities:
                js_resumes = list(object_list.exclude(id__in=response_resumes_ids).filter(user=jobseeker.user))
                new_resumes.extend(js_resumes)
            resumes = new_resumes

        jobseekers, cities = [], []
        for resume in resumes:
            jobseeker = JobSeeker.objects.get(user=resume.user)
            jobseekers.append(jobseeker)
            cities.append(jobseeker.city)

        responses_cities = sorted(Counter(cities).items(), key=lambda x: x[1], reverse=True)[:4]
        responses_cities.insert(0, (self.TOTAL_K, len(object_list)))

        return resumes, jobseekers, responses_cities


class ResumeDetailView(LoginRequiredMixin, DetailView):
    """View for getting detail info in resume."""

    model = models.Resume
    extra_context = {'title': 'Резюме'}

    def get_context_data(self, **kwargs):
        context = super(ResumeDetailView, self).get_context_data()
        context['jobs'] = context['resume'].jobs.all()
        context['jobseeker'] = JobSeeker.objects.get(user=context['resume'].user)
        if self.request.user.status == UserStatusChoices.EMPLOYER:
            from recruiting.models import Response
            notifs = [notif for notif in self.request.user.notifications.unread()
                      if notif.verb == NEW_RESUME_NOTIF]
            notifs_resumes = [notif.target for notif in notifs]
            if (resume := context['object']) in notifs_resumes:
                notifs[notifs_resumes.index(resume)].mark_as_read()
            if self.request.user in resume.favourites.all():
                context['fav'] = True
            if Response.objects.filter(resume=context['resume']).exists() and \
                    'vac_id' in self.request.GET:
                context['response'] = Response.objects.get(resume=context['resume'],
                                                           vacancy__id=self.request.GET['vac_id'])
        return context


class ResumeCreateView(CreateView):
    model = Resume
    form_class = ResumeForm
    success_url = reverse_lazy("resumes:resume_list")
    template_name = "resumes/resume_create.html"
    extra_context = {'title': 'Создание Резюме'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resume_form'] = context['form']
        context['contacts_form'] = forms.ContactsForm(self.request.POST)
        context['position_form'] = forms.PositionForm(self.request.POST)
        context['experience_form'] = forms.ExperienceForm(self.request.POST)
        return context

    def get_form_kwargs(self):
        kwargs = super(ResumeCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    @transaction.atomic
    def get_form(self, form_class=None):
        form = super(ResumeCreateView, self).get_form(form_class=form_class)
        if self.request.method == 'POST':
            contacts_form = forms.ContactsForm(self.request.POST)
            position_form = forms.PositionForm(self.request.POST)
            experience_form = forms.ExperienceForm(self.request.POST)
            if experience_form.is_valid():
                form.instance.experience_id = experience_form.save().id
                form.errors.pop('experience')
            if position_form.is_valid():
                form.instance.position_id = position_form.save().id
                form.errors.pop('position')
            if contacts_form.is_valid():
                form.instance.contacts_id = contacts_form.save().id
                form.errors.pop('contacts')
            form.instance.user_id = self.request.user.id
        return form


class ResumeUpdateView(LoginRequiredMixin, ResumeCreateView, UpdateView):
    """View for updating resume."""
    template_name = "resumes/resume_update.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume = context['object']
        context['resume_form'] = context['form']
        context['contacts_form'] = forms.ContactsForm(initial=model_to_dict(resume.contacts))
        context['position_form'] = forms.PositionForm(initial=model_to_dict(resume.position))
        context['experience_form'] = forms.ExperienceForm(initial=model_to_dict(resume.experience))
        return context

    def get(self, request, *args, **kwargs):
        return super(UpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(UpdateView, self).post(request, *args, **kwargs)


class ResumeDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting resume."""

    model = models.Resume
    success_url = reverse_lazy('resumes:resume_list')


class ContactsDetailView(LoginRequiredMixin, DetailView):
    """View for getting detail information about contacts in resume."""

    model = models.Contacts


class ContactsUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating contacts in resume."""

    model = models.Contacts
    form_class = forms.ContactsForm
    success_url = reverse_lazy('resumes:resume_list')


class PositionDetailView(LoginRequiredMixin, DetailView):
    """View for getting detail information about position in resume."""

    model = models.Position


class PositionUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating position in resume."""

    model = models.Position
    form_class = forms.PositionForm
    success_url = reverse_lazy('resumes:resume_list')


class ExperienceDetailView(LoginRequiredMixin, DetailView):
    """View for getting detail information about experience in resume."""

    model = models.Experience


class ExperienceUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating experience in resume."""

    model = models.Experience
    form_class = forms.ExperienceForm
    success_url = reverse_lazy('resumes:resume_list')


class JobCreateView(LoginRequiredMixin, CreateView):
    model = models.Job
    form_class = forms.JobForm
    success_url = reverse_lazy('resumes:resume_list')
    extra_context = {'title': 'Добавление нового места работы'}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(JobCreateView, self).form_valid(form)


class JobDetailView(LoginRequiredMixin, DetailView):
    """View for getting detail information about jobs in resume."""

    model = models.Job


class JobUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating jobs in resume."""

    model = models.Job
    form_class = forms.JobForm
    template_name = 'resumes/job_update.html'
    success_url = reverse_lazy('resumes:resume_list')

    def get_context_data(self, **kwargs):
        context = super(JobUpdateView, self).get_context_data(**kwargs)
        context['title'] = str(context['object'])
        return context
