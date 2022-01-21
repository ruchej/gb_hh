from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm

from .models import Account


class UserRegisterForm(UserCreationForm, PasswordResetForm):
    class Meta:
        model = Account
        fields = (
            "username",
            "first_name",
            "last_name",
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
            PasswordResetForm.save(self, **kwargs)
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
