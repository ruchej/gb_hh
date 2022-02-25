from django.contrib.auth.models import AnonymousUser

from conf.choices import UserStatusChoices
from chat.views import NEW_MESSAGE
from recruiting.views import NEW_RESUME_NOTIF


def new_messages(request):
    if not isinstance(request.user, AnonymousUser):
        new_messages = [True for notif in request.user.notifications.unread() if notif.verb == NEW_MESSAGE]
        return {'new_messages': len(new_messages)}
    return {'new_messages': 0}


def new_responses(request):
    if not isinstance(request.user, AnonymousUser) and request.user.status == UserStatusChoices.EMPLOYER:
        new_responses = [True for notif in request.user.notifications.unread() if notif.verb == NEW_RESUME_NOTIF]
        return {'new_responses': len(new_responses)}
    return {'new_responses': 0}


def user_status_choices(request):
    return {
        'user_status_choices': UserStatusChoices
    }
