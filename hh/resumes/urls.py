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
    path('search/', views.ResumeListView.as_view(), name='resume_list_search'),
    path('<int:pk>/', views.ResumeDetailView.as_view(), name='resume_detail'),
    path('create/', views.ResumeCreateView.as_view(), name='resume_create'),
    path('update/<int:pk>/', views.ResumeUpdateView.as_view(), name='resume_update'),
    path('delete/<int:pk>/', views.ResumeDeleteView.as_view(), name='resume_delete'),
    path('contacts/<int:pk>/', views.ContactsDetailView.as_view(), name='contacts_detail'),
    path('contacts/update/<int:pk>/', views.ContactsUpdateView.as_view(), name='contacts_update'),
    path('position/<int:pk>/', views.PositionDetailView.as_view(), name='position_detail'),
    path('position/update/<int:pk>/', views.PositionUpdateView.as_view(), name='position_update'),
    path('experience/<int:pk>/', views.ExperienceDetailView.as_view(), name='experience_detail'),
    path('experience/update/<int:pk>/', views.ExperienceUpdateView.as_view(), name='experience_update'),
    path('job/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('job/create/', views.JobCreateView.as_view(), name='job_create'),
    path('job/update/<int:pk>/', views.JobUpdateView.as_view(), name='job_update'),
    path('favorites_resumes/', views.resume_favorite_list, name='favorites_resumes'),
]
