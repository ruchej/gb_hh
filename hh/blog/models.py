from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1000)
    short_description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Новости'
        ordering = ['created_at']
