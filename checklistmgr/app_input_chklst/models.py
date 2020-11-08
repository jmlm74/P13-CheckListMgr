from django.db import models
from django.db.models import UniqueConstraint

from app_user.models import Company, Address


class Manager(models.Model):
    """
    Manager model -->
    Foreign key : Address and Company
    Can be disabled --> not usable in checklist input
    """
    mgr_name = models.CharField(max_length=30, verbose_name="Owner")
    mgr_contact = models.CharField(max_length=30, verbose_name="Contact", null=True, blank=True)
    mgr_phone = models.CharField(max_length=31, verbose_name="Phone", null=True, blank=True)
    mgr_email1 = models.EmailField(max_length=255, verbose_name='Email1', null=True, blank=True)
    mgr_email2 = models.EmailField(max_length=255, verbose_name='Email2', null=True, blank=True)
    mgr_enable = models.BooleanField(verbose_name="Enable", default=True)

    mgr_company = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name="mgr_company", null=True)
    mgr_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name="mgr_address",
                                    null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = "Manager"
        verbose_name_plural = "Managers"
        constraints = [
            UniqueConstraint(fields=['mgr_name', 'mgr_company'], name='Unique mgr/society'),
        ]
        ordering = ['mgr_company', 'mgr_name']
        indexes = [
            models.Index(fields=['mgr_company'], name='I_Mgr_Company'),
        ]

    def __str__(self):
        return self.mgr_name

    def __repr__(self):
        return self.mgr_name


class Material(models.Model):
    """
    Material -->
    Foreign key : Manager, company Material --> a material may be on another material
    --> IE A TAIL LIFT ON A TRUCK --> 2 materials : The truck (primary) then the tail lift (secondary)
    Can be disabled --> not usable in checklist input
    """
    mat_designation = models.CharField(max_length=30, verbose_name="Naming")
    mat_registration = models.CharField(max_length=30, verbose_name="Serial", null=True, blank=True)
    mat_type = models.CharField(max_length=30, verbose_name="Type", null=True, blank=True)
    mat_model = models.CharField(max_length=30, verbose_name="Model", null=True, blank=True)
    mat_enable = models.BooleanField(verbose_name="Enable", default=True)

    mat_manager = models.ForeignKey(Manager, on_delete=models.RESTRICT, related_name="mat_manager")
    mat_material = models.ForeignKey('self', on_delete=models.RESTRICT, related_name="mat_secondary",
                                     null=True)
    mat_company = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name="mat_company", null=True)

    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"
        constraints = [
            UniqueConstraint(fields=['mat_designation', 'mat_manager'], name='Unique materiel/manager'),
        ]
        ordering = ['mat_manager', 'mat_designation']
        indexes = [
            models.Index(fields=['mat_manager'], name='I_Mat_Manager'),
        ]

    def __str__(self):
        return self.mat_designation
