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

app_name = 'resumes'

urlpatterns = [
    path('', views.ResumeListView.as_view(), name='resume_list'),
    path('', views.ResumeDetailView.as_view(), name='resume_detail'),
    path('', views.ResumeCreateView.as_view(), name='resume_create'),
    path('', views.ResumeUpdateView.as_view(), name='resume_update'),
    path('', views.ResumeDeleteView.as_view(), name='resume_delete'),
    path('', views.PersonalInfoDetailView.as_view(), name='personal_info_detail'),
    path('', views.PersonalInfoUpdateView.as_view(), name='personal_info_update'),
    path('', views.ContactsDetailView.as_view(), name='contacts_detail'),
    path('', views.ContactsUpdateView.as_view(), name='contacts_update'),
    path('', views.PositionDetailView.as_view(), name='position_detail'),
    path('', views.PositionUpdateView.as_view(), name='position_update'),
    path('', views.ExperienceDetailView.as_view(), name='experience_detail'),
    path('', views.ExperienceUpdateView.as_view(), name='experience_update'),
    path('', views.JobDetailView.as_view(), name='job_detail'),
    path('', views.JobUpdateView.as_view(), name='job_update'),
]
