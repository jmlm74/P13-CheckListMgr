from datetime import datetime

from django.db import models
from django.db.models import UniqueConstraint

from app_create_chklst.models import CheckList
from app_input_chklst.models import Material, Manager
from app_user.models import User, Company


def cld_default_id():
    return str(datetime.now().timestamp())[:15]


class CheckListDone(models.Model):
    """
    Checklist
    """
    cld_status = models.PositiveSmallIntegerField(default=0, verbose_name="Status")
    cld_key = models.CharField(max_length=15, verbose_name="Key", null=True,
                               default=cld_default_id)
    cld_mail_sent = models.BooleanField(default=False, verbose_name='Mail sent')
    cld_pdf_file = models.FileField(upload_to="checklists/%Y/%m/",
                                    max_length=100,
                                    verbose_name='PDF Filename',
                                    null=True)
    cld_mat = models.CharField(max_length=30, verbose_name="Material", null=True)
    cld_man = models.CharField(max_length=30, verbose_name="Manager", null=True)
    cld_valid = models.BooleanField(default=False, verbose_name="Valid")
    cld_remarks = models.TextField(verbose_name="Remarks", null=True)

    cld_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="cld_user", null=True)
    cld_checklist = models.ForeignKey(CheckList, on_delete=models.SET_NULL, related_name='cld_checklist', null=True)
    cld_material = models.ForeignKey(Material, on_delete=models.SET_NULL, related_name='cld_material', null=True)
    cld_manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, related_name='cld_manager', null=True)
    cld_company = models.ForeignKey(Company, on_delete=models.SET_NULL, related_name='cld_company', null=True)

    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = "Check-List Done"
        verbose_name_plural = "Check-Lists Done"
        constraints = [
            UniqueConstraint(fields=['cld_key', 'cld_company'], name='Unique key/society'),
        ]
        ordering = ['cld_company', 'cld_key']
        indexes = [
            models.Index(fields=['cld_company'], name='I_cld_Company'),
        ]

    def __str__(self):
        return str(self.id)


class CheckListPhoto(models.Model):
    pho_caption = models.CharField(max_length=30, verbose_name='Caption', null=True)
    pho_file = models.ImageField(upload_to='photos/%Y/%m/', max_length=100, verbose_name='Photo')

    pho_chklst_done = models.ForeignKey(CheckListDone, on_delete=models.CASCADE, related_name='pho_chklst')

    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return str(self.id)
