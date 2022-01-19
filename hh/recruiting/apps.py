from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RecruitingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recruiting'
    verbose_name = _('рекрутинг')
