from django.contrib import admin

from . import models


@admin.register(models.Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'telegram',)
    list_per_page = 15
    search_fields = ('email', )


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'salary', 'employment_type', 'relocation', 'business_trip',)
    list_filter = ('salary',)
    list_per_page = 15
    search_fields = ('title', )


@admin.register(models.Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('about', 'skills', 'portfolio',)
    list_filter = ('skills',)
    list_per_page = 15


@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('organization', 'start', 'end', 'city', 'site', 'scope', 'position', 'functions',)
    list_filter = ('start', 'end', 'city')
    list_per_page = 15
    search_fields = ('organization',)


@admin.register(models.Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'photo', 'contacts', 'position', 'experience',)
    list_select_related = ('contacts', 'position', 'experience',)
    list_per_page = 15
    search_fields = ('user', 'title',)
