from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, DetailView
from django.utils.translation import gettext_lazy as _
from .models import Account
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView
from .forms import UserRegisterForm, UserActivationRegisterForm


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
    template_name = '../templates/login.html'
    success_message = _("Вход в систему выполнен")
    extra_context = {
        "page_title": _("Login"),
        "header_class": "hero",
        "content_class": "tab-content",
    }

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data()
        context.update({'title': 'Вход'})
        return context


class Logout(UserAuthMixin, LogoutView):
    success_message = _("Вы вышли из системы")

    def get_next_page(self):
        messages.success(self.request, self.success_message)
        return super().get_next_page()


class UserCreate(
    UserNotAuthMixin,
    SuccessMessageMixin,
    CreateView,
    PasswordResetView,
):
    model = Account
    extra_context = {
        "page_title": _("Форма регистрации"),
        "header_class": "hero",
    }
    form_class = UserRegisterForm
    """
    Registration User with send email and post activation (SignUpConfirmView)
    """
    success_url = reverse_lazy("accounts:Login")
    url_redirect = reverse_lazy("accounts:UserDetail")
    template_name = "registration/registration.html"
    email_template_name = "accounts/signup_email.html"
    success_message = _("Для активации аккаунта выслано письмо")


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
    extra_context = {
        "page_title": _("Профиль пользователя"),
        "header_class": "hero",
    }

    def get_object(self, *args, **kwargs):
        return self.request.user
