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

from . import views

app_name = 'recruiting'

urlpatterns = [
    path('responses/', views.ResponseListView.as_view(), name='response_list'),
    path('responses/search/', views.ResponseListView.as_view(), name='response_list_search'),
    path('responses/notif/get/', views.get_notifications, name='get_notif'),
    path('responses/create/<int:v_pk>/', views.ResponseCreateView.as_view(), name='response_create'),
    path('responses/create/<int:r_pk>/<int:v_pk>/', views.ResponseCreateView.as_view(), name='response_create_submit'),
    path('responses/accept/<int:r_pk>/', views.response_accept, name='response_accept'),
    path('responses/reject/<int:r_pk>/', views.response_reject, name='response_reject'),
    path('responses/delete/<int:pk>/', views.ResponseDeleteView.as_view(), name='response_delete'),
]
