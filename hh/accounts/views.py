from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, DetailView
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
from .forms import UserRegisterForm, UserActivationRegisterForm
from django.views.generic.edit import FormView


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
        else:
            raise Exception('Undefined user status')
        return account

