from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    admin = models.BooleanField(default=False, verbose_name="is admin")
    phone = models.CharField(max_length=31, blank=True, null=True, verbose_name="Phone number")
    picture = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100,
                                blank=True, null=True, verbose_name="photo or avatar")


    def __str__(self):
        return self.username

