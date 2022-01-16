from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from . import models


class ResumeListView(LoginRequiredMixin, ListView):
    model = models.Resume
    template_name = 'brief-list.html'

    def get_context_data(self, **kwargs):
        context = super(ResumeListView, self).get_context_data()
        context.update({'title': 'Резюме'})
        return context
