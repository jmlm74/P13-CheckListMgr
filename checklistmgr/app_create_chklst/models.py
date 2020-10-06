from django.db import models
from django.db.models import UniqueConstraint

from app_user.models import User, Company
from app_utilities.models import Translation


class Line(models.Model):
    class LineType(models.TextChoices):
        CHOICE = "C", Translation.get_translation("Checkbox", language="UK")
        TEXT = "T", Translation.get_translation("Text", language="UK")

    line_key = models.CharField(max_length=30, verbose_name='Line key')
    line_wording = models.CharField(max_length=80, verbose_name='Line title')
    line_enable = models.BooleanField(verbose_name='Line enabled', default=True)
    line_type = models.CharField(max_length=1,
                                 verbose_name="Line Type",
                                 choices=LineType.choices,
                                 default=LineType.CHOICE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    line_company = models.ForeignKey(Company, related_name='line', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Line'
        verbose_name_plural = 'Lines'
        constraints = [
            UniqueConstraint(fields=['line_key', 'line_company'], name='Unique line/society'),
        ]
        ordering = ['line_company', 'line_key']
        indexes = [
            models.Index(fields=['line_company'], name='I_Line_Company'),
        ]

    def __str__(self):
        return self.line_key


class Category(models.Model):
    cat_key = models.CharField(max_length=30, verbose_name='Category key')
    cat_wording = models.CharField(max_length=80, verbose_name='Category title')
    cat_enable = models.BooleanField(verbose_name='Category enabled', default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    cat_company = models.ForeignKey(Company, related_name='category', on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            UniqueConstraint(fields=['cat_key', 'cat_company'], name='Unique category/society'),
        ]
        ordering = ['cat_company', 'cat_key']
        indexes = [
            models.Index(fields=['cat_company'], name='I_Cat_Company'),
        ]

    def __str__(self):
        return self.cat_key


class CheckList(models.Model):
    chk_key = models.CharField(max_length=30, verbose_name='Check-List key')
    chk_title = models.CharField(max_length=80, verbose_name='Check-List title')
    chk_enable = models.BooleanField(verbose_name='Check-List enabled')
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    chk_company = models.ForeignKey(Company, related_name='ckecklist', on_delete=models.CASCADE)
    chk_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    chk_category = models.ManyToManyField(Category,
                                          through='CheckListCategory',
                                          related_name='checklist',
                                          blank=True,
                                          default=None,
                                          symmetrical=False)
    chk_line = models.ManyToManyField(Line,
                                      through='CheckListLine',
                                      related_name='checklist',
                                      blank=True,
                                      default=None,
                                      symmetrical=False)

    class Meta:
        verbose_name = 'Check-List'
        verbose_name_plural = 'Check-Lists'
        UniqueConstraint(fields=['chk_key', 'chk_company'], name='Unique checklist/society')
        ordering = ['chk_company', 'chk_key']
        indexes = [
            models.Index(fields=['chk_company'], name='I_Chk_Company')
        ]

    def __str__(self):
        return self.chk_key


class CheckListCategory(models.Model):
    chk_cat_position = models.PositiveSmallIntegerField(verbose_name='Category Position')
    chk_cat_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='clc_categories')
    chk_cat_checklist = models.ForeignKey(CheckList, on_delete=models.CASCADE, related_name='clc_checklists')


class CheckListLine(models.Model):
    chk_line_position = models.PositiveSmallIntegerField(verbose_name='Line Position')
    chk_line_category = models.ForeignKey(Line, on_delete=models.CASCADE, related_name='cll_categories')
    chk_line_checklist = models.ForeignKey(CheckList, on_delete=models.CASCADE, related_name='cll_checklists')
