from django import forms

from . import models


class PersonalInfoForm(forms.ModelForm):
    model = models.PersonalInfo
    fields = ('name', 'patronymic', 'surname', 'birthday', 'gender', 'location', 'relocation', 'business_trip')


class ContanctsForm(forms.ModelForm):
    model = models.Contacts
    fields = ('phone', 'email', 'telegram')


class PositionForm(forms.ModelForm):
    model = models.Position
    fields = ('title', 'salary', 'employment', 'schedule')


class ExperienceFprm(forms.ModelForm):
    model = models.Experience
    fields = ('skills', 'about', 'portfolio')


class JobForm(forms.ModelForm):
    model = models.Job
    fields = ('organization', 'start', 'end', 'location', 'site', 'scope', 'position', 'functions')
