from django.views.generic import ListView

from . import models


class ResumeListView(ListView):
    model = models.Resume
    template_name = 'brief-list.html'
