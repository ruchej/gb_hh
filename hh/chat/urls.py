"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import ChatListView, ChatAcceptView, accept_chat, open_chat, receive_message, search_contact, \
    read_notifications, get_notifications, create_reject_chat, ChatRejectView

app_name = 'chat'

urlpatterns = [
    path('', ChatListView.as_view(), name='list'),

    path('resume-invite/<int:resume_id>', ChatAcceptView.as_view(), name='start_resume'),
    path('response-accept/<int:response_id>', ChatAcceptView.as_view(), name='start_response'),
    path('create/<int:user_id>/', accept_chat, name='accept'),

    path('response-reject/<int:response_id>', ChatRejectView.as_view(), name='start_reject'),
    path('reject/<int:user_id>/', create_reject_chat, name='reject'),

    path('open/<int:chat_id>/', open_chat, name='open'),
    path('search-contact/', search_contact, name='search_contact'),
    path('receive/<int:chat_id>/', receive_message, name='receive'),
    path('notif/read/<int:chat_id>/', read_notifications, name='read_notif'),
    path('notif/get/', get_notifications, name='get_notif'),
]
