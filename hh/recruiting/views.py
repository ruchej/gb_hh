from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView

from . import models
from accounts.models import JobSeeker


class ResponseListView(LoginRequiredMixin, ListView):
    """View for getting list of responses for job."""

    model = models.Response
    extra_context = {'title': 'Отклики'}
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ResponseListView, self).get_context_data(object_list=object_list, **kwargs)
        jobseekers = []
        for response in context['response_list']:
            jobseekers.append(JobSeeker.objects.get(user=response.resume.user))
        context['jobseekers_resp_list'] = list(zip(jobseekers, context['response_list']))
        return context

    def get_queryset(self):
        return super().get_queryset().filter(vacancy__employer=self.request.user)


class ResponseCreateView(LoginRequiredMixin, CreateView):
    """View for creating response for job."""

    model = models.Response


class ResponseDeleteView(LoginRequiredMixin, CreateView):
    """View for deleting response for job."""

    model = models.Response


class OfferListView(LoginRequiredMixin, ListView):
    """View for getting list of offers."""

    model = models.Offer


class OfferCreateView(LoginRequiredMixin, CreateView):
    """View for creating offer."""

    model = models.Offer


class OfferDeleteView(LoginRequiredMixin, CreateView):
    """View for deleting offer."""

    model = models.Offer
