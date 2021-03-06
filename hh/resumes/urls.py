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
    path('job/create/', views.JobCreateView.as_view(), name='job_create'),
    path('job/update/<int:pk>/', views.JobUpdateView.as_view(), name='job_update'),
    path('job/delete/<int:pk>/', views.JobDeleteView.as_view(), name='job_delete'),
    path('favorites_resumes/', views.resume_favorite_list, name='favorites_resumes'),
]
