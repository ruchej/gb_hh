from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView

from . import models


class ResponseListView(LoginRequiredMixin, ListView):
    """View for getting list of responses for job."""

    model = models.Response
    extra_context = {'title': 'Отклики'}
    paginate_by = 10

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
