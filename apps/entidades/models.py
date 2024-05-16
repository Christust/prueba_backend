from django.db import models
from apps.base.models import Base


# Create your models here.
class Maestro(Base):
    nombre_completo = models.CharField(
        "Nombre completo",
        max_length=100,
        null=False,
        blank=False,
        default="nombre default",
    )
    sueldo = models.FloatField("Sueldo", null=False, blank=False, default=1000)

    def natural_key(self):
        return self.nombre_completo

    def __str__(self):
        return f"{self.nombre_completo}"

    class Meta:
        verbose_name = "Maestro"
        verbose_name_plural = "Maestros"


class Salon(models.Model):
    codigo = models.CharField(primary_key=True, max_length=3, null=False, blank=False)
    letra = models.CharField(
        "Letra",
        max_length=100,
        null=False,
        blank=False,
        default="A",
    )
    maestro = models.ForeignKey(
        Maestro, on_delete=models.CASCADE, null=True, blank=True
    )

    def natural_key(self):
        return self.letra

    def __str__(self):
        return f"{self.letra}"

    class Meta:
        verbose_name = "Salon"
        verbose_name_plural = "Salones"
