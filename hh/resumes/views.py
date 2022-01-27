from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from . import models, forms
from accounts.models import UserStatus


class ResumeListView(LoginRequiredMixin, ListView):
    """View for getting list of all resumes."""

    model = models.Resume
    extra_context = {'title': 'Мои Резюме'}
    paginate_by = 10

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
        return context


class ResumeCreateView(LoginRequiredMixin, CreateView):
    """View for creating resume."""
    model = models.Resume
    # form_class = forms.PersonalInfoForm


class ResumeUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating resume."""

    model = models.Resume
    # form_class = forms.PersonalInfoForm


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
