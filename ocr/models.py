from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import *
import datetime
import os
from django.conf import settings


class OrganoAcademico(models.Model):
    """Entidad que agrupa departamentos/coordinaciones en divisiones/decanatos

    Sus atributos son el nombre del órgano y el tipo (Decanato, Divisón u Otro).
    Se utilizará principalemente para organización interna de las unidades que manejen
    programas de estudio.
    """

    class Meta:
        verbose_name = "órgano académico"
        verbose_name_plural = "órganos académicos"

    nombre                                              = models.CharField(
        max_length=70,
        help_text="El nombre completo del órgano académico",
        verbose_name="nombre")
    tipo                                                = models.CharField(
        max_length=4,
        choices=(('Deca', 'Decanato'),
                ('Divi', 'División'),
                ('Otro', 'Otro')),
        help_text="El tipo de órgano académico (decanato, división, etc.)",
        verbose_name="tipo")

    def __str__(self):
        return self.nombre


class UnidadAcademica(models.Model):
    """Entidad (como un departamento) que maneja programas de estudio

    Sus atributos son el nombre de la unidad y los órganos a los que está adscrita.
    Esta relación es de N a N, pues un órgano tiene varias unidades y la misma
    puede pertenecer a varios órganos.
    """

    class Meta:
        verbose_name = "unidad académica"
        verbose_name_plural = "unidades académicas"

    nombre                                              = models.CharField(
        max_length=40,
        help_text="El nombre completo de la unidad académica",
        verbose_name="nombre")
    organo                                              = models.ManyToManyField(OrganoAcademico,
        help_text="Relación de pertencia a órgano académico",
        verbose_name="organos",
        related_name="adscritoa")

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        os.mkdir(settings.MEDIA_ROOT+"/"+self.nombre)
        super(UnidadAcademica,self).save(*args, **kwargs)



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
        max_length=40,
        help_text="El nombre completo de la materia",
        verbose_name="nombre")
    fecha_periodo                                       = models.CharField(
        max_length=1,
        choices=(('1','Enero-Marzo'),
                ('2','Abril-Julio'),
                ('3','Verano'),
                ('4','Septiembre-Diciembre')),
        help_text="El trimestre cuando entra en vigencia el programa",
        verbose_name="trimestre")
    fecha_año                                           = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1967)],
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
    departamento                                        = models.ForeignKey(
        UnidadAcademica, on_delete=models.CASCADE,
        help_text="El departamento responsable por la asignatura",
        verbose_name="departamento")
    def determinar_lugar(instance, filename):
        """Callable para determinar lugar apropiado en el FS para el PDF subido."""
        dept = UnidadAcademica.objects.get(programa__codigo=instance.codigo)
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


class Requisito(models.Model):
    """Entidad relacionada a Programa (N a 1); se refiere a las materias requisito para el curso

    Sus atributos son el texto que señala el requisito, así como el programa al
    al cual se refiere."""

    class Meta:
        order_with_respect_to = "programa"
        verbose_name = "requisito"
        verbose_name_plural = "requisitos"

    texto                                               = models.CharField(
        max_length=500,
        help_text="Un requisito de la asignatura (para un programa específico)",
        verbose_name="requisito")
    programa                                            = models.ForeignKey(
        Programa, on_delete=models.CASCADE,
        help_text="El programa de la asignatura que lo requiere",
        verbose_name="programa")

    def __str__(self):
        """Imprime como parte inicial del texto"""
        return self.texto[:30]


class ReferenciaBibliografica(models.Model):
    """Entidad relacionada a PRograma (N a 1); se refiere a libros u otro material de apoyo en el curso.

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
