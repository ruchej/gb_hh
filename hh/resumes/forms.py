from django import forms
from django.forms import DateInput
from django.forms.models import inlineformset_factory

from . import models


class ResumeForm(forms.ModelForm):
    """Form for processing information about resume."""

    class Meta:
        model = models.Resume
        fields = ('title', 'photo')


class ContactsForm(forms.ModelForm):
    """Form for processing information about contacts in resume."""

    class Meta:
        model = models.Contacts
        fields = ('phone', 'email', 'telegram')


class PositionForm(forms.ModelForm):
    """Form for processing information about position in resume."""

    class Meta:
        model = models.Position
        fields = ('title', 'salary', 'employment_type', 'relocation', 'business_trip')


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
