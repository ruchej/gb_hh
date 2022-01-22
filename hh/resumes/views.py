from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from . import models, forms


class ResumeListView(LoginRequiredMixin, ListView):
    """View for getting list of all resumes."""

    model = models.Resume
    template_name = 'resumes/list.html'
    extra_context = {'title': 'Резюме'}


class ResumeDetailView(LoginRequiredMixin, DetailView):
    """View for getting detail info in resume."""

    model = models.Resume
    template_name = 'brief-detail.html'


class ResumeCreateView(LoginRequiredMixin, CreateView):
    """View for creating resume."""
    model = models.Resume
    template_name = 'brief-create.html'


class ResumeUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating resume."""

    model = models.Resume
    template_name = 'brief-update.html'


class ResumeDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting resume."""

    model = models.Resume
    template_name = 'brief-delete.html'


class PersonalInfoDetailView(LoginRequiredMixin, DetailView):
    """View for getting detail information about personal info in resume."""

    model = models.PersonalInfo
    form_class = forms.PersonalInfoForm
    template_name = 'personal-info-detail.html'


class PersonalInfoUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating personal info in resume."""

    model = models.PersonalInfo
    form_class = forms.PersonalInfoForm
    template_name = 'personal-info-update.html'


class ContactsDetailView(LoginRequiredMixin, DetailView):
    """View for getting detail information about contacts in resume."""

    model = models.Contacts
    form_class = forms.ContactsForm
    template_name = 'contacts-detail.html'


class ContactsUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating contacts in resume."""

    model = models.Contacts
    form_class = forms.ContactsForm
    template_name = 'contacts-update.html'


class PositionDetailView(LoginRequiredMixin, DetailView):
    """View for getting detail information about position in resume."""

    model = models.Position
    form_class = forms.PositionForm
    template_name = 'position-detail.html'


class PositionUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating position in resume."""

    model = models.Position
    form_class = forms.PositionForm
    template_name = 'position-update.html'


class ExperienceDetailView(LoginRequiredMixin, DetailView):
    """View for getting detail information about experience in resume."""

    model = models.Experience
    form_class = forms.ExperienceForm
    template_name = 'experience-detail.html'


class ExperienceUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating experience in resume."""

    model = models.Experience
    form_class = forms.ExperienceForm
    template_name = 'experience-update.html'


class JobDetailView(LoginRequiredMixin, DetailView):
    """View for getting detail information about jobs in resume."""

    model = models.Job
    form_class = forms.JobForm
    template_name = 'job-detail.html'


class JobUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating jobs in resume."""

    model = models.Job
    form_class = forms.JobForm
    template_name = 'job-update.html'
