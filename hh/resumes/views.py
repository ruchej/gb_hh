from collections import Counter

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from el_pagination.views import AjaxListView
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from . import models, forms
from accounts.models import UserStatus, JobSeeker


def resume_favorite_list(request):
    user = request.user
    favorites_resumes = user.favourites_resumes.all()
    context = {
        'favorites_resumes': favorites_resumes,
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
        if self.request.user.status == UserStatus.JOBSEEKER:
            context['object_list'] = self.employee_filter(context, object_list)
            context['jobseeker'] = JobSeeker.objects.get(user=self.request.user)
        else:
            context['title'] = 'Резюме Соискателей'
            resumes, jobseekers, context['resumes_cities'] = self.employer_filter(context, object_list)
            favs = [True if self.request.user in resume.favourites.all() else False for resume in resumes]
            context['jobseekers_resume_list'] = list(zip(jobseekers, resumes, favs))
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.status == UserStatus.JOBSEEKER:
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
                resumes = self.model.objects.filter(position__salary=int(text))
            else:
                resumes = self.model.objects.filter(
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
                    js_resumes = list(self.model.objects.filter(user=jobseeker.user))
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
                js_resumes = list(self.model.objects.filter(user=jobseeker.user))
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
        context['jobs'] = models.Job.objects.filter(experience=context['resume'].experience)
        context['jobseeker'] = JobSeeker.objects.get(user=context['resume'].user)
        if self.request.user.status == UserStatus.EMPLOYER:
            notifs = [notif for notif in self.request.user.notifications.unread()]
            notifs_resumes = [notif.target for notif in notifs]
            if (resume := context['object']) in notifs_resumes:
                notifs[notifs_resumes.index(resume)].mark_as_read()
        return context


@login_required
def resume_create(request):
    if request.method == 'POST':
        resume_form = forms.ResumeForm(request.POST)
        contacts_form = forms.ContactsForm(request.POST)
        position_form = forms.PositionForm(request.POST)
        experience_form = forms.ExperienceForm(request.POST)
        job_form = forms.JobForm(request.POST)
        view_forms = (resume_form, contacts_form, position_form, experience_form, job_form)
        if all([item.is_valid() for item in view_forms]):
            resume_form.form.save(commit=False)
            resume_form.user = request.user
            for item in view_forms[1:]:
                item.save()
        return render(request, 'resumes/resume_create.html')
    else:
        resume_form = forms.ResumeForm()
        contacts_form = forms.ContactsForm()
        position_form = forms.PositionForm()
        experience_form = forms.ExperienceForm()
        job_form = forms.JobForm()
    return render(request, 'resumes/resume_create.html', {
        'resume_form': resume_form,
        'contacts_form': contacts_form,
        'position_form': position_form,
        'experience_form': experience_form,
        'job_form': job_form,
    })


class ResumeUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating resume."""

    model = models.Resume
    form_class = forms.ResumeForm


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


class JobDetailView(LoginRequiredMixin, DetailView):
    """View for getting detail information about jobs in resume."""

    model = models.Job


class JobUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating jobs in resume."""

    model = models.Job
    form_class = forms.JobForm
    success_url = reverse_lazy('resumes:resume_list')
