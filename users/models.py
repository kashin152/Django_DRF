from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomsUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(upload_to="photo/avatar", blank=True, null=True, verbose_name="Аватар",
                               help_text="Загрузите аватар")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email