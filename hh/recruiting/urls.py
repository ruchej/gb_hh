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
    path('response-list/', views.ResponseListView.as_view(), name='response_list'),
    path('response-create/<int:pk>/', views.ResponseCreateView.as_view(), name='response_create'),
    path('response-delete/<int:pk>/', views.ResponseDeleteView.as_view(), name='response_delete'),
    path('offer-list/', views.OfferListView.as_view(), name='offer_list'),
    path('offer-create/<int:pk>/', views.OfferCreateView.as_view(), name='offer_create'),
    path('offer-delete/<int:pk>/', views.OfferDeleteView.as_view(), name='offer_delete'),
]
