from django.db import models
from django.core.exceptions import ObjectDoesNotExist





# Create your models here.


# Create your models here.
class Translation(models.Model):
    """
        Translate model
        Position is the key
        FR and UK are the translations. The key may be also a message

        Method get_translation
            Args :
                position --> the key to get
                language --> the language translation to return
            Return
                The value get for the specified language
    """
    Position = models.CharField(max_length=100, verbose_name='Field Position', unique=True)
    FR = models.TextField(verbose_name='French Text')
    UK = models.TextField(verbose_name='English Text')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Translation"
        indexes = [
            models.Index(fields=['Position'], name='I_Position'),
        ]
        ordering = ['Position']

    def __str__(self):
        return f"{self.Position} - {self.FR} - {self.UK}"

    @classmethod
    def get_translation(cls, position, **kwargs):
        from app_user.models import User
        if 'username' in kwargs:
            user = User.objects.filter(username=kwargs['username'])
            if user:
                language = user[0].preferred_language.code
            else:
                language = 'UK'
        else:
            if 'language' in kwargs:
                language = kwargs['language']
            else:
                language = 'UK'
        try:
            text_dict = Translation.objects.values(language).get(Position=position)
            text = text_dict[language]
        except ObjectDoesNotExist:
            text = f"Error -{position}- Not found!!!!"
        return text

