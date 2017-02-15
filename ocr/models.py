from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import *
import datetime

# Create your models here.
class OrganoAcademico(models.Model):
    nombre = models.CharField(max_length=70, help_text="El nombre completo del órgano académico", verbose_name="nombre")
    TIPO = (
        ('Deca', 'Decanato'),
        ('Divi', 'División'),
        ('Otro', 'Otro')
    )
    tipo = models.CharField(max_length=4, choices=TIPO, help_text="El tipo de órgano académico (decanato, división, etc.)", verbose_name="tipo")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "órgano académico"
        verbose_name_plural = "órganos académicos"



class UnidadAcademica(models.Model):
    nombre = models.CharField(max_length=40, help_text="El nombre completo de la unidad académica", verbose_name="nombre")
    organo = models.ManyToManyField(OrganoAcademico, help_text="Relación de pertencia a órgano académico", verbose_name="organos")

    def __str__(self):
        return self.nombre

    class Meta:
    #    order_with_respect_to = "organo"
        verbose_name = "unidad académica"
        verbose_name_plural = "unidades académicas"


class Programa(models.Model):
    codigo = models.CharField(max_length=6, validators=[RegexValidator(regex='^([A-Z0-9]){6}$')],
                                help_text="El código de la materia", verbose_name="código")
    denominacion = models.CharField(max_length=40, help_text="El nombre completo de la materia", verbose_name="nombre")
    PERIODOS = (
        ('1', 'Enero-Marzo'),
        ('2', 'Abril-Julio'),
        ('3', 'Verano'),
        ('4', 'Septiembre-Diciembre')
    )
    fecha_periodo       = models.CharField(max_length=1, choices=PERIODOS,
                                help_text="El trimestre cuando entra en vigencia el programa", verbose_name="trimestre")
    fecha_año           = models.PositiveSmallIntegerField(validators=[MinValueValidator(1967)],
                                help_text="El año cuando entra en vigencia el programa", verbose_name="año")
    horas_teoria        = models.PositiveSmallIntegerField(help_text="El número de horas de teoría semanales", verbose_name="horas de teoría")
    horas_practica      = models.PositiveSmallIntegerField(help_text="El número de horas de práctica semanales", verbose_name="horas de práctica")
    horas_laboratorio   = models.PositiveSmallIntegerField(help_text="El número de horas de laboratorio semanales", verbose_name="horas de laboratorio")
    creditos            = models.PositiveSmallIntegerField(validators=[MaxValueValidator(16)],
                                help_text="La cantidad de créditos que vale la materia", verbose_name="créditos")
    # requisitos (Otra tabla, 1aN)
    objetivos                   = models.TextField(help_text="Los objetivos de la materia", verbose_name="objetivos")
    contenidos_sinopticos       = models.TextField(help_text="Resumen del contenido de la materia", verbose_name="contenido")
    estrategias_metodologicas   = models.TextField(help_text="Las estratégias metodológicas de enseñanza utilizadas", verbose_name="estretegias metodológicas")
    estrategias_evaluacion      = models.TextField(help_text="Las estrategias de evaluación utilizadas", verbose_name="estrategias de evaluación")
    # bibliografia (Otra tabla, 1aN)
    departamento = models.ForeignKey(UnidadAcademica, on_delete=models.CASCADE,
                                help_text="El departamento responsable por la asignatura", verbose_name="departamento")
    def determinar_lugar(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        dept = UnidadAcademica.objects.get(programa__codigo=instance.codigo)
        periodo = instance.fecha_periodo
        if periodo[0] == 'E':   periodo="EM"
        elif periodo[0] == 'A': periodo="AJ"
        elif periodo[0] == 'V': periodo="VE"
        else:                   periodo="SD"
        return "%s/%s-%s-%s.pdf" % (dept, instance.codigo, instance.fecha_año, periodo)
    pdf = models.FileField(upload_to=determinar_lugar, help_text="El PDF del programa a analizar", verbose_name="pdf")

    def __str__(self):
        return self.codigo + " (" + self.PERIODOS[int(self.fecha_periodo)][1] + " " + str(self.fecha_año) + ")"

    class Meta:
        unique_together = ("codigo", "fecha_periodo", "fecha_año")
        verbose_name = "programa"
        ordering = ["departamento", "fecha_año", "fecha_periodo"]

    def clean_pdf(self):
        files = self.cleaned_data.get('pdf')
        for f in files:
            if f:
                if f._size > 20*1024*1024:
                    raise forms.ValidationError("El archivo es demasiado grande ( > 20MB ).")
            else:
                raise forms.ValidationError("No se pudo leer el archivo.")
        return files

    def clean(self):
        ht = self.horas_teoria
        hp = self.horas_practica
        hl = self.horas_laboratorio
        fa = self.fecha_año
        if not (ht and hp and hl and fa):
            raise ValidationError('Falta información')
        if ht + hp + hl > 40:
            raise ValidationError('Un programa no debe tener más de 40 horas semanales (en total)')
        if fa > datetime.datetime.now().year+1:
            raise ValidationError('No está permitido registrar programas que aun no entran en vigencia')


class Requisito(models.Model):
    texto       = models.CharField(max_length=500, help_text="Un requisito de la asignatura (para un programa específico)", verbose_name="requisito")
    programa    = models.ForeignKey(Programa, on_delete=models.CASCADE, help_text="El programa de la asignatura que lo requiere", verbose_name="programa")

    def __str__(self):
        return self.texto[:30]

    class Meta:
        order_with_respect_to = "programa"
        verbose_name = "requisito"
        verbose_name_plural = "requisitos"


class ReferenciaBibliografica(models.Model):
    texto       = models.CharField(max_length=500, help_text="Una fuente bibliográfica recomendada", verbose_name="referencia")
    programa    = models.ForeignKey(Programa, on_delete=models.CASCADE, help_text="El prgrama que la recomienda", verbose_name="programa")

    def __str__(self):
        return self.texto[:30]

    class Meta:
        order_with_respect_to = "programa"
        verbose_name = "referencia"
        verbose_name_plural = "referencias"