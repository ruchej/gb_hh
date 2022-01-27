from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from .models import Account, UserStatus, JobSeeker, Employer
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView, PasswordContextMixin
from .forms import UserRegisterForm, UserActivationRegisterForm, JobSeekerFormUpdate, AccountFormUpdate, \
    EmployerFormUpdate


class UserNotAuthMixin(UserPassesTestMixin):
    url_redirect = "/"
    warning_message = _("Эта опция доступна только для новых посетителей.")

    def test_func(self):
        return self.request.user.is_anonymous

    def handle_no_permission(self):
        messages.warning(self.request, self.warning_message)
        return HttpResponseRedirect(self.url_redirect)


class UserAuthMixin(UserNotAuthMixin):
    warning_message = _("Для перехода по этой ссылке пожалуйста залогиньтесь.")

    def test_func(self):
        return self.request.user.is_authenticated


class Login(SuccessMessageMixin, UserNotAuthMixin, LoginView):
    success_message = _("Вход в систему выполнен")
    extra_context = {
        "title": _("Вход"),
        "header_class": "hero",
        "content_class": "tab-content",
    }


class Logout(UserAuthMixin, LogoutView):
    success_message = _("Вы вышли из системы")

    def get_next_page(self):
        messages.success(self.request, self.success_message)
        return super().get_next_page()


class UserCreate(
    UserNotAuthMixin,
    SuccessMessageMixin,
    # PasswordResetView,
    CreateView,
):
    model = Account
    extra_context = {"title": _("Регистрация")}
    form_class = UserRegisterForm
    success_url = reverse_lazy("blog:news")
    #url_redirect = reverse_lazy("accounts:UserDetail")
    template_name = 'accounts/account_signup_form.html'
    success_message = _("Для активации аккаунта выслано письмо")

    def get_form_kwargs(self):
        form_kwargs = super(UserCreate, self).get_form_kwargs()
        form_kwargs['new_status_choices'] = UserStatus.choices
        form_kwargs['new_status_choices'].pop(UserStatus.MODERATOR)
        return form_kwargs


class UserConfirm(PasswordResetConfirmView):
    """
    Activation accounts
    """

    extra_context = {
        "page_title": _("Подтверждение регистрации"),
        "header_class": "hero",
    }

    success_url = reverse_lazy("accounts:Login")
    template_name = "accounts/signup_confirm.html"
    form_class = UserActivationRegisterForm
    post_reset_login = True
    post_reset_login_backend = "django.contrib.auth.backends.ModelBackend"
    INTERNAL_RESET_URL_TOKEN = "set-active"


class UserDetail(LoginRequiredMixin, DetailView):
    """
    Профиль пользователя
    """

    model = Account
    extra_context = {"title": _("Профиль")}
    template_name = 'accounts/detail.html'

    def get_object(self, *args, **kwargs):
        if self.request.user.status == UserStatus.JOBSEEKER:
            account = JobSeeker.objects.get(user=self.request.user)
        elif self.request.user.status == UserStatus.EMPLOYER:
            account = Employer.objects.get(user=self.request.user)
        elif self.request.user.status == UserStatus.MODERATOR:
            account = Account.objects.get(user=self.request.user)
        else:
            raise Exception('Undefined user status')
        return account


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Account
    success_url = reverse_lazy("accounts:UserDetail")
    success_message = _('Профиль изменен')
    template_name = 'accounts/profile_update.html'
    form_class = AccountFormUpdate
    jobseeker_form_class = JobSeekerFormUpdate
    employer_form_class = EmployerFormUpdate
    extra_context = {'title': 'Изменение Профиля'}

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        if self.request.user.status == 1:
            jobseeker = JobSeeker.objects.get(user=self.request.user)
            context['jobseeker_form'] = self.jobseeker_form_class(instance=jobseeker)
        elif self.request.user.status == 2:
            employer = Employer.objects.get(user=self.request.user)
            context['employer_form'] = self.employer_form_class(instance=employer)
        return context

    @transaction.atomic
    def form_valid(self, form):
        jobseeker_form = None
        employer_form = None
        try:
            jobseeker_form = JobSeekerFormUpdate(
                data=self.request.POST,
                instance=JobSeeker.objects.get(user=self.request.user)
            )
        except Exception:
            pass
        try:
            employer_form = EmployerFormUpdate(
                data=self.request.POST,
                instance=Employer.objects.get(user=self.request.user)
            )
        except Exception:
            pass
        form_valid = False
        if jobseeker_form and jobseeker_form.is_valid():
            jobseeker_form.save()
            form_valid = True
        if employer_form and employer_form.is_valid():
            employer_form.save()
            form_valid = True
        if form_valid:
            form.save()
        return super(ProfileUpdateView, self).form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user
