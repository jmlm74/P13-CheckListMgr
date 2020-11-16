from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class Address(models.Model):
    """
    Address -> Same model for companies addresses or managers
    """
    address_name = models.CharField(max_length=50, verbose_name="Mnemonic address name")
    street_number = models.PositiveSmallIntegerField(default=0, verbose_name="Street Number")
    street_type = models.CharField(max_length=20, blank=True, default="", verbose_name="Street Type")
    address1 = models.CharField(max_length=150, blank=True, default="", verbose_name="Address 1")
    address2 = models.CharField(max_length=150, blank=True, default="", verbose_name="Address 2")
    zipcode = models.CharField(max_length=20, blank=True, default="", verbose_name="Zip Code")
    city = models.CharField(max_length=50, blank=True, default="", verbose_name="City")
    country = models.CharField(max_length=40, blank=True, default="", verbose_name="Country")
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.address_name


class UserLanguages(models.Model):
    """
    Language code : FR - Francais....
    """
    code = models.CharField(max_length=2, verbose_name='Language code', default='FR', unique=True, primary_key=True)
    language = models.CharField(max_length=20, verbose_name='Language', default='Francais')

    class Meta:
        verbose_name = "User Languages"
        verbose_name_plural = "User Languages"

    def __str__(self):
        return self.code


class Company(models.Model):
    """
    Company
    Just a name and an address (what else ?)
    """
    company_name = models.CharField(max_length=100,
                                    verbose_name="Society",
                                    unique=True)
    address = models.ForeignKey(Address, on_delete=models.RESTRICT, related_name="society", null=True, blank=True,
                                verbose_name="Address")
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        # indexes = [models.Index(fields=(['name']), name='I_company_name')]
        ordering = ['company_name']

    def __str__(self):
        return self.company_name


class User(AbstractUser):
    """
    User model --> inheri AbstractUser
    The email is here to be unique --> reset password !!!!
    admin --> just admin for the app not is_admin !
    pro --> Professional user
    Picture : An avatar but not really used !
    """
    email = models.EmailField(max_length=255, unique=True, verbose_name='Email')
    admin = models.BooleanField(default=False, verbose_name="is admin")
    pro = models.BooleanField(default=False, verbose_name="is pro")
    phone = models.CharField(max_length=31, blank=True, null=True, verbose_name="Phone number")
    picture = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=100,
                                blank=True, null=True, verbose_name="Picture")
    first_login = models.BooleanField(default=True)
    preferred_language = models.ForeignKey(UserLanguages, on_delete=models.CASCADE, related_name='user_language',
                                           default=None, null=True)
    user_company = models.ForeignKey(Company, on_delete=models.RESTRICT, related_name='user_company',
                                     default=None, null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return "{} - {}".format(self.first_name, self.last_name)
