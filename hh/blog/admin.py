from django.contrib import admin
from .models import Article


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'author', 'created_at', 'updated_at', 'is_active')


# Register your models here.
admin.site.register(Article, NewsAdmin)
