from re import T
from django.db import models
from django.urls import reverse


# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')
    short_description = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='blog/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'post_id': self.pk})

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Новости'
        ordering = ['created_at']
