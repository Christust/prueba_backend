from django.db import models


# Create your models here.
class Base(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)

    class Meta:
        abstract = True
        verbose_name = "Modelo base"
        verbose_name_plural = "Modelos base"
