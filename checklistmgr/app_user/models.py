from django.contrib.auth.models import AbstractUser
from app_utilities.models import Address
from django.db import models




class UserLanguages(models.Model):
    code = models.CharField(max_length=2, verbose_name='Language code', default='FR', unique=True, primary_key=True)
    language = models.CharField(max_length=20, verbose_name='Language', default='Francais')

    class Meta:
        verbose_name = "User Languages"
        verbose_name_plural = "User Languages"

    def __str__(self):
        return self.code


class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name="Society", unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="society", null=True, blank=True,
                                verbose_name="Address")

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        # indexes = [models.Index(fields=(['name']), name='I_company_name')]
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):

    admin = models.BooleanField(default=False, verbose_name="is admin")
    phone = models.CharField(max_length=31, blank=True, null=True, verbose_name="Phone number")
    picture = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=100,
                                blank=True, null=True, verbose_name="Picture")
    preferred_language = models.ForeignKey(UserLanguages, on_delete=models.CASCADE, related_name='user_language',
                                           default=None, null=True)
    user_company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='user_company',
                                     default=None, null=True, blank=True)



    def __str__(self):
        return self.username




