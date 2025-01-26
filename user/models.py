from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator, URLValidator


class User(AbstractUser):
    email = models.EmailField(
        validators=[EmailValidator(message="Некорректный формат email.")],
        verbose_name="Email"
    )
    home_page = models.URLField(
        blank=True,
        null=True,
        validators=[URLValidator(message="Некорректный формат URL.")],
        verbose_name="Домашняя страница"
    )

    def __str__(self):
        return self.username
