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
import notifications.urls
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from accounts.views import EmployerDetailView


app_name = 'conf'

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('resumes/', include('resumes.urls', namespace='resumes')),
    path('vacancies/', include('vacancies.urls', namespace='vacancies')),
    path('', include('blog.urls', namespace='blog')),
    path('recruiting/', include('recruiting.urls', namespace='recruiting')),
    path('employer/<int:pk>/', EmployerDetailView.as_view(), name='employer_detail'),
    path('rules/',
         TemplateView.as_view(template_name='rules.html',
                              extra_context={'title': 'Правила портала'}),
         name='rules'),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
