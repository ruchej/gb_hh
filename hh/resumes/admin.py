from django.contrib import admin

from . import models


@admin.register(models.PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('display_full_name', 'birthday', 'gender', 'location', 'relocation', 'business_trip')
    list_filter = ('birthday', 'gender',)
    list_per_page = 15
    search_fields = ('surname', )


@admin.register(models.Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'telegram',)
    list_per_page = 15
    search_fields = ('email', )


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'salary', 'employment', 'schedule',)
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
    list_display = ('organization', 'start', 'end', 'location', 'site', 'scope', 'position', 'functions',)
    list_filter = ('start', 'end', 'location')
    list_per_page = 15
    search_fields = ('organization',)


@admin.register(models.Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'photo', 'personal_info', 'contacts', 'position', 'experience',)
    list_select_related = ('personal_info', 'contacts', 'position', 'experience',)
    list_per_page = 15
    search_fields = ('title',)
