from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from companys.models import Company

User = get_user_model()

class Profile(models.Model):
    class ROLE_CHOICES(models.TextChoices):
        USER = 'user',
        ADMIN = 'admin',

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=20,
                            choices=ROLE_CHOICES.choices,
                            default=ROLE_CHOICES.USER)
    company = models.ForeignKey(Company, verbose_name='Компания', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def is_admin(self):
        if self.role == 'admin' or self.is_superuser:
            return True
        return False
