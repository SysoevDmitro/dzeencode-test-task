from django.db import models
from django.conf import settings


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,  # Для анонимных пользователей
        blank=True
    )
    username = models.CharField(max_length=50, null=True, blank=True, verbose_name="Имя пользователя")
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    text = models.TextField(verbose_name="Текст комментария")
    home_page = models.URLField(null=True, blank=True, verbose_name="Домашняя страница")
    captcha = models.CharField(max_length=6, verbose_name="Капча")
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username or self.user.username
