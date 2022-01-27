from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from . import models, forms
from accounts.models import UserStatus, JobSeeker


class ResumeListView(LoginRequiredMixin, ListView):
    """View for getting list of all resumes."""

    model = models.Resume
    extra_context = {'title': 'Мои Резюме'}
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ResumeListView, self).get_context_data(object_list=object_list, **kwargs)
        context['jobseeker'] = JobSeeker.objects.get(user=self.request.user)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.status == UserStatus.JOBSEEKER:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class ResumeDetailView(LoginRequiredMixin, DetailView):
    """View for getting detail info in resume."""

    model = models.Resume
    extra_context = {'title': 'Резюме'}

    def get_context_data(self, **kwargs):
        context = super(ResumeDetailView, self).get_context_data()
        context['jobs'] = models.Job.objects.filter(experience=context['resume'].experience)
        context['jobseeker'] = JobSeeker.objects.get(user=context['resume'].user)
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
