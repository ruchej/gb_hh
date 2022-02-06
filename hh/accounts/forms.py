from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm, UserChangeForm
from django.forms import DateInput
from cities_light.models import Country, City
import floppyforms

from .models import Account, JobSeeker, Employer


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = Account
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "status"
        )

    def __init__(self, *args, **kwargs):
        new_status_choices = kwargs.pop('new_status_choices')
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = new_status_choices
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.help_text = ""

    def save(self, commit=True, **kwargs):
        user = self.instance
        if not user.id:
            user.active = False
            user = super().save()
        return user


class UserActivationRegisterForm(forms.Form):
    class Meta:
        model = Account

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.user.active = True
        if commit:
            self.user.save()
        return self.user


class AccountFormUpdate(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            'username',
            'email',
            'password',
            'avatar'
        )


class JobSeekerFormUpdate(forms.ModelForm):
    class Meta:
        model = JobSeeker
        fields = (
            'first_name',
            'patronymic',
            'last_name',
            'sex',
            'date_birth',
            'phone',
            'address'
        )
        widgets = {
            'date_birth': DateInput(attrs={'type': 'date'})
        }


class EmployerFormUpdate(forms.ModelForm):
    class Meta:
        model = Employer
        fields = (
            'name',
            'description',
            'phone',
            'country',
            'city',
            'address'
        )
        widgets = {
            'country': floppyforms.widgets.Input(
                datalist=Country.objects.all
            ),
            'city': floppyforms.widgets.Input(
                datalist=City.objects.all
            )
        }
