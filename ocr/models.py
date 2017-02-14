from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import *
import datetime

# Create your models here.
class OrganoAcademico(models.Model):
    nombre = models.CharField(max_length=70)
    TIPO = (
        ('Deca', 'Decanato'),
        ('Divi', 'División'),
        ('Otro', 'Otro')
    )
    tipo = models.CharField(max_length=4, choices=TIPO)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "organo académico"
        verbose_name_plural = "organos académicos"


class UnidadAcademica(models.Model):
    nombre = models.CharField(max_length=40)
    organo = models.ManyToManyField(OrganoAcademico)

    def __str__(self):
        return self.nombre

    class Meta:
        order_with_respect_to = "organo"
        verbose_name = "unidad académica"
        verbose_name_plural = "unidades académicas"


class Programa(models.Model):
    codigo = models.CharField(max_length=6, validators=[RegexValidator(regex='^([A-Z0-9]){6}$')])
    denominacion = models.CharField(max_length=40)
    PERIODOS = (
        ('1', 'Enero-Marzo'),
        ('2', 'Abril-Julio'),
        ('3', 'Verano'),
        ('4', 'Septiembre-Diciembre')
    )
    fecha_periodo       = models.CharField(max_length=1, choices=PERIODOS)
    fecha_año           = models.PositiveSmallIntegerField(validators=[MinValueValidator(1967)])
    horas_teoria        = models.PositiveSmallIntegerField()
    horas_practica      = models.PositiveSmallIntegerField()
    horas_laboratorio   = models.PositiveSmallIntegerField()
    creditos            = models.PositiveSmallIntegerField(validators=[MinValueValidator(16)])
    # requisitos (Otra tabla, 1aN)
    objetivos                   = models.TextField()
    contenidos_sinopticos       = models.TextField()
    estrategias_metodologicas   = models.TextField()
    estrategias_evaluacion      = models.TextField()
    # bibliografia (Otra tabla, 1aN)
    departamento = models.ForeignKey(UnidadAcademica, on_delete=models.CASCADE)

    def __str__(self):
        return self.codigo + " (" + fecha_periodo + " " + fecha_año + ")"

    def determinar_lugar(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        dept = UnidadAcademica.objects.filter(programa__codigo=instance.codigo)
        periodo = instance.periodo
        if periodo[0] == 'E':
            periodo="EM"
        elif periodo[0] == 'A':
            periodo="AJ"
        elif periodo[0] == 'V':
            periodo="VE"
        else:
            periodo="SD"
        return "%s/%s-%s%s" % dept, instance.codigo, instance.fecha_año, periodo

    class Meta:
        unique_together = ("codigo", "fecha_periodo", "fecha_año")
        verbose_name = "programa"
        ordering = ["departamento", "fecha_año", "fecha_periodo"]

    def clean(self):
        if self.horas_teoria + self.horas_practica + self.horas_laboratorio > 40:
            raise ValidationError('Un programa no debe tener más de 40 horas semanales (en total)')
        if self.fecha_año > datetime.datetime.now().year+1:
            raise ValidationError('No está permitido registrar programas que aun no entran en vigencia')


class Requisito(models.Model):
    texto       = models.CharField(max_length=300)
    programa    = models.ForeignKey(Programa, on_delete=models.CASCADE)

    def __str__(self):
        return self.texto[:30]

    class Meta:
        order_with_respect_to = "programa"
        verbose_name = "requisito"
        verbose_name_plural = "requisitos"


class ReferenciaBibliografica(models.Model):
    texto       = models.CharField(max_length=500)
    programa    = models.ForeignKey(Programa, on_delete=models.CASCADE)

    def __str__(self):
        return self.texto[:30]

    class Meta:
        order_with_respect_to = "programa"
        verbose_name = "referencia"
        verbose_name_plural = "referencias"