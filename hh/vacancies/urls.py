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

from .views import VacancyList, VacancyDetail, VacancyCreate, VacancyUpdate, VacancyDelete, favorites_vacancies_list

app_name = 'vacancies'

urlpatterns = [
    path('', VacancyList.as_view(), name='vacancy_list'),
    path('search/', VacancyList.as_view(), name='vacancy_list_search'),
    path('<int:pk>/detail/', VacancyDetail.as_view(), name='detail'),
    path('create/', VacancyCreate.as_view(), name='create'),
    path('create/employer/<int:pk>/', VacancyCreate.as_view(), name='create_vacancy'),
    path('<int:pk>/update/', VacancyUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', VacancyDelete.as_view(), name='delete'),
    path('favorites_vacancies/', favorites_vacancies_list, name='favorites_vacancies'),
]
