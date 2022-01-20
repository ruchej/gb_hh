from django import forms

from . import models


class PersonalInfoForm(forms.ModelForm):
    """Form for processing information about personal information in resume."""
    class Meta:
        model = models.PersonalInfo
        fields = ('name', 'patronymic', 'surname', 'birthday', 'gender', 'location', 'relocation', 'business_trip')


class ContactsForm(forms.ModelForm):
    """Form for processing information about contacts in resume."""

    class Meta:
        model = models.Contacts
        fields = ('phone', 'email', 'telegram')


class PositionForm(forms.ModelForm):
    """Form for processing information about position in resume."""

    class Meta:
        model = models.Position
        fields = ('title', 'salary', 'employment', 'schedule')


class ExperienceForm(forms.ModelForm):
    """Form for processing information about experience in resume."""

    class Meta:
        model = models.Experience
        fields = ('skills', 'about', 'portfolio')


class JobForm(forms.ModelForm):
    """Form for processing information about jobs in resume."""

    class Meta:
        model = models.Job
        fields = ('organization', 'start', 'end', 'location', 'site', 'scope', 'position', 'functions')
