from django import forms
from django.forms import DateInput
from django.forms.models import inlineformset_factory

from . import models


class ResumeForm(forms.ModelForm):
    """Form for processing information about resume."""

    class Meta:
        model = models.Resume
        fields = ('title', 'photo', 'contacts', 'position', 'experience', 'jobs')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ResumeForm, self).__init__(*args, **kwargs)
        self.fields['jobs'].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields['jobs'].queryset = models.Job.objects.filter(user=user)
        self.fields['jobs'].widget.attrs['form'] = 'resume_form'


class ContactsForm(forms.ModelForm):
    """Form for processing information about contacts in resume."""

    class Meta:
        model = models.Contacts
        fields = ('phone', 'email', 'telegram')


class PositionForm(forms.ModelForm):
    """Form for processing information about position in resume."""

    class Meta:
        model = models.Position
        fields = ('position', 'salary', 'employment_type', 'relocation', 'business_trip')


class ExperienceForm(forms.ModelForm):
    """Form for processing information about experience in resume."""

    class Meta:
        model = models.Experience
        fields = ('skills', 'about', 'portfolio')


class JobForm(forms.ModelForm):
    """Form for processing information about jobs in resume."""

    class Meta:
        model = models.Job
        fields = ('organization', 'start', 'end', 'city', 'site', 'scope', 'position', 'functions')
        widgets = {
            'start': DateInput(attrs={'type': 'date'}),
            'end': DateInput(attrs={'type': 'date'}),
        }
