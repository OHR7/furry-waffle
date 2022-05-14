from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    last_updated = models.DateField(null=True)
    kudos_counter = models.IntegerField(default=3, validators=[MinValueValidator(0), MaxValueValidator(3)])
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username


class Organization(models.Model):
    name = models.CharField(max_length=30)
