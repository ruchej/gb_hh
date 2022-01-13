from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from . import models


class ResumeListView(LoginRequiredMixin, ListView):
    model = models.Resume
    template_name = 'brief-list.html'
