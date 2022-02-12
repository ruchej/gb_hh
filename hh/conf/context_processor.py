from accounts.models import UserStatus
from chat.views import NEW_MESSAGE
from recruiting.views import NEW_RESUME_NOTIF


def new_messages(request):
    new_messages = [True for notif in request.user.notifications.unread() if notif.verb == NEW_MESSAGE]
    return {'new_messages': len(new_messages)}


def new_responses(request):
    if request.user.status != UserStatus.EMPLOYER:
        return {'new_responses': 0}
    new_responses = [True for notif in request.user.notifications.unread() if notif.verb == NEW_RESUME_NOTIF]
    return {'new_responses': len(new_responses)}
