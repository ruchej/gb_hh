from django import forms

from .models import Vacancy


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = (
            'title',
            'description',
            'hashtags',
            'employment_type',
            'experience',
            'salary',
        )
