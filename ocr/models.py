from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import *
import datetime
import os
from ocr.validators import validate_pdf_ext_mime
from django.conf import settings


class Instancia(models.Model):
    """Instancia responsable del programa de estudio.
    """

    class Meta:
        verbose_name = "instancia"
        verbose_name_plural = "instancias"

    nombre                                              = models.CharField(
        max_length=40,
        help_text="El nombre completo de la unidad académica",
        verbose_name="nombre")

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        os.mkdir(settings.MEDIA_ROOT+"/"+self.nombre)
        super(Instancia,self).save(*args, **kwargs)



class Programa(models.Model):
    """Programa de estudio. Identificado por Código y Fecha

    Sus atributos son el código del curso para el cual el programa funciona
    (el cual sigue el formato regular de códigos de asignaturas), el nombre o
    denominación de dicho curso, la fecha en la que entra en vigencia el programa
    (periodo académico, o trimestre, y año), la cantidad de horas de teoría, práctica
    y laboratorio semanales de la asignatura (juntas no deben ser más de 40),
    la cantidad de créditos que vale la materia y el departamento (clave foránea)
    que la regula.

    Incluye atributos opcionales, como los objetivos de la asignatura, el contenido
    sinóptico, estratégias metodológicas y de evaluación.

    Todo:
        * Move help_text to help_texts in Form only

    """

    class Meta:
        unique_together = ("codigo", "fecha_periodo", "fecha_año")
        verbose_name = "programa"

    codigo                                              = models.CharField(
        max_length=6,
        validators=[RegexValidator(regex='^([A-Z0-9]){6}$')],
        help_text="El código de la materia",
        verbose_name="código")
    denominacion                                        = models.CharField(
        max_length=100,
        help_text="El nombre completo de la materia",
        verbose_name="nombre")
    fecha_periodo                                       = models.CharField(
        max_length=1,
        choices=(('1','ene-mar'),
                ('2','abr-jul'),
                ('3','intensivo'),
                ('4','sep-dic')),
        help_text="El trimestre cuando entra en vigencia el programa",
        verbose_name="trimestre")
    fecha_año                                           = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1969)],
        help_text="El año cuando entra en vigencia el programa",
        verbose_name="año")
    horas_teoria                                        = models.PositiveSmallIntegerField(
        help_text="El número de horas de teoría semanales",
        verbose_name="horas de teoría")
    horas_practica                                      = models.PositiveSmallIntegerField(
        help_text="El número de horas de práctica semanales",
        verbose_name="horas de práctica")
    horas_laboratorio                                   = models.PositiveSmallIntegerField(
        help_text="El número de horas de laboratorio semanales",
        verbose_name="horas de laboratorio")
    creditos                                            = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(16)],
        help_text="La cantidad de créditos que vale la materia",
        verbose_name="créditos")
    objetivos                                           = models.TextField(
        help_text="Los objetivos de la materia",
        verbose_name="objetivos")
    contenidos_sinopticos                               = models.TextField(
        help_text="Resumen del contenido de la materia",
        verbose_name="contenido")
    estrategias_metodologicas                           = models.TextField(
        help_text="Las estratégias metodológicas de enseñanza utilizadas",
        verbose_name="estretegias metodológicas")
    estrategias_evaluacion                              = models.TextField(
        help_text="Las estrategias de evaluación utilizadas",
        verbose_name="estrategias de evaluación")
    requisito                                           = models.TextField(
        help_text="Requisitos para cursar la materia",
        verbose_name="requisito")
    instancia                                           = models.ForeignKey(
        Instancia, on_delete=models.CASCADE,
        help_text="Instancia responsable por la asignatura",
        verbose_name="instancia")
    def determinar_lugar(instance, filename):
        """Callable para determinar lugar apropiado en el FS para el PDF subido."""
        dept = Instancia.objects.get(programa__codigo=instance.codigo)
        periodo = instance.fecha_periodo
        if periodo[0] == 'E':   periodo="EM"
        elif periodo[0] == 'A': periodo="AJ"
        elif periodo[0] == 'V': periodo="VE"
        else:                   periodo="SD"
        return "%s/%s-%s-%s.pdf" % (dept, instance.codigo, instance.fecha_año, periodo)
    pdf                                                 = models.FileField(
        upload_to=determinar_lugar,
        help_text="El PDF del programa a analizar",
        verbose_name="pdf")

    def __str__(self):
        """Imprime como '[Código] ([Periodo (dos letras)] [año (0000)])''"""
        return self.codigo + " (" + self.PERIODOS[int(self.fecha_periodo)][1] + " " + str(self.fecha_año) + ")"
        ordering = ["departamento", "fecha_año", "fecha_periodo"]

    def clean_pdf(self):
        """Rechaza archivos mayores a un tamaño límite (20MB)."""
        files = self.cleaned_data.get('pdf')
        for f in files:
            if f:
                if f._size > 20*1024*1024:
                    raise forms.ValidationError("El archivo es demasiado grande ( > 20MB ).")
            else:
                raise forms.ValidationError("No se pudo leer el archivo.")
        return files

    def clean(self):
        """Rechaza guardar Programas sin horas asignadas, o que las mismas sean demasiadas."""
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


class PDFAnonimo(models.Model):
    """Entidad para el manejo de PDFs subidos previo al ingreso de información extra

    Sus atributos son el pdf como string al archivo en el FS, el tipo de PDF (
    texto seleccionable o simple escaneo) y el texto extraído del PDF utilizando las
    herramientas incluídas."""

    pdf                                                 = models.FileField(
        validators=[validate_pdf_ext_mime],
        upload_to='tmp',
        help_text="El PDF del programa a analizar",
        verbose_name="pdf")
    tipo                                                = models.CharField(
        max_length=1,
        choices=(('T','Texto'),('I','Imagen')),
        help_text="El tipo de PDF a analizar",
        verbose_name="tipo")
    texto                                               = models.TextField(
        help_text="El texto extraído del PDF",
        verbose_name="texto extraído",
        blank=True)

    def __str__(self):
        """Imprime como nombre del PDF"""
        return self.pdf.name



class ReferenciaBibliografica(models.Model):
    """Entidad relacionada a Programa (N a 1); se refiere a libros u otro material de apoyo en el curso.

    Sus atributos son el texto que señala la referencia bibliográfica, así como el
    programa al cual se refiere."""

    class Meta:
        order_with_respect_to = "programa"
        verbose_name = "referencia"
        verbose_name_plural = "referencias"

    texto                                               = models.CharField(
        max_length=500,
        help_text="Una fuente bibliográfica recomendada",
        verbose_name="referencia")
    programa                                            = models.ForeignKey(
        Programa, on_delete=models.CASCADE,
        help_text="El prgrama que la recomienda",
        verbose_name="programa")

    def __str__(self):
        """Imprime como un extracto de la referencia"""
        return self.texto[:30]


class Programa_Borrador(models.Model):

    class Meta:
        unique_together = ("codigo", "fecha_periodo", "fecha_año")
        verbose_name = "programa_borrador"

    codigo                                              = models.CharField(
        max_length=6,
        validators=[RegexValidator(regex='^([A-Z0-9]){6}$')],
        help_text="El código de la materia",
        verbose_name="código")
    denominacion                                        = models.CharField(
        max_length=100,
        help_text="El nombre completo de la materia",
        verbose_name="nombre",
        blank=True,
        null=True)
    fecha_periodo                                       = models.CharField(
        max_length=1,
        choices=(('1','ene-mar'),
                ('2','abr-jul'),
                ('3','intensivo'),
                ('4','sep-dic')),
        help_text="El trimestre cuando entra en vigencia el programa",
        verbose_name="trimestre")
    fecha_año                                           = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1969)],
        help_text="El año cuando entra en vigencia el programa",
        verbose_name="año")
    horas_teoria                                        = models.PositiveSmallIntegerField(
        help_text="El número de horas de teoría semanales",
        verbose_name="horas de teoría",
        blank=True,
        null=True)
    horas_practica                                      = models.PositiveSmallIntegerField(
        help_text="El número de horas de práctica semanales",
        verbose_name="horas de práctica",
        blank=True,
        null=True)
    horas_laboratorio                                   = models.PositiveSmallIntegerField(
        help_text="El número de horas de laboratorio semanales",
        verbose_name="horas de laboratorio",
        blank=True,
        null=True)
    creditos                                            = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(16)],
        help_text="La cantidad de créditos que vale la materia",
        verbose_name="créditos",
        blank=True,
        null=True)
    objetivos                                           = models.TextField(
        help_text="Los objetivos de la materia",
        verbose_name="objetivos",
        blank=True,
        null=True)
    contenidos_sinopticos                               = models.TextField(
        help_text="Resumen del contenido de la materia",
        verbose_name="contenido",
        blank=True,
        null=True)
    estrategias_metodologicas                           = models.TextField(
        help_text="Las estratégias metodológicas de enseñanza utilizadas",
        verbose_name="estretegias metodológicas",
        blank=True,
        null=True)
    estrategias_evaluacion                              = models.TextField(
        help_text="Las estrategias de evaluación utilizadas",
        verbose_name="estrategias de evaluación",
        blank=True,
        null=True)
    instancia                                           = models.ForeignKey(
        Instancia, on_delete=models.CASCADE,
        help_text="Instancia responsable por la asignatura",
        verbose_name="instancia")
    def determinar_lugar(instance, filename):
        """Callable para determinar lugar apropiado en el FS para el PDF subido."""
        dept = Instancia.objects.get(programa__codigo=instance.codigo)
        periodo = instance.fecha_periodo
        if periodo[0] == 'E':   periodo="EM"
        elif periodo[0] == 'A': periodo="AJ"
        elif periodo[0] == 'V': periodo="VE"
        else:                   periodo="SD"
        return "%s/%s-%s-%s.pdf" % (dept, instance.codigo, instance.fecha_año, periodo)
    pdf                                                 = models.FileField(
        upload_to=determinar_lugar,
        help_text="El PDF del programa a analizar",
        verbose_name="pdf")

    def __str__(self):
        """Imprime como '[Código] ([Periodo (dos letras)] [año (0000)])''"""
        return self.codigo + " (" + self.PERIODOS[int(self.fecha_periodo)][1] + " " + str(self.fecha_año) + ")"
        ordering = ["departamento", "fecha_año", "fecha_periodo"]

    def clean_pdf(self):
        """Rechaza archivos mayores a un tamaño límite (20MB)."""
        files = self.cleaned_data.get('pdf')
        for f in files:
            if f:
                if f._size > 20*1024*1024:
                    raise forms.ValidationError("El archivo es demasiado grande ( > 20MB ).")
            else:
                raise forms.ValidationError("No se pudo leer el archivo.")
        return files
