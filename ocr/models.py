"""Modelos de la Base de Datos

Se tienen Decanato (o Divisón), Instancia (Reponsable), Programa (Completo),
Programa_Borrador (incompleto), PDFAnonimo (para PDF que no tienen asignado un borrador aun)
TipoCampoAdicional (para agrupar campos adicionales), CampoAdicional,
SeccionFuenteInformacion, AutorReferencia y ReferenciaBibliografica.
"""

import datetime, os
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import *
from django.conf import settings
from ocr.validators import validate_pdf_ext_mime

class Decanato(models.Model):
    """Decanato o Division en las que se agrupan las instancias responsables.

    De atributo tiene el nombre del decanato o división.
    """

    class Meta:
        verbose_name = "Decanato"
        verbose_name_plural = "Decanato"

    nombre                                              = models.CharField(
        max_length=40,
        help_text="El nombre completo del decanato o division",
        verbose_name="nombre")

    def __str__(self):
        return self.nombre

class Instancia(models.Model):
    """Instancia responsable del programa de estudio.

    Como atributo tiene el nombre de la instancia responsable y la referencia al
    decanato o divisón al que pertenece.
    """

    class Meta:
        verbose_name = "instancia"
        verbose_name_plural = "instancias"

    nombre                                              = models.CharField(
        max_length=40,
        help_text="El nombre completo de la unidad académica",
        verbose_name="nombre")

    decanato                                            = models.ManyToManyField(
        Decanato, #on_delete=models.CASCADE,
        help_text="Decanato o Division a la que pertenece la Unidad",
        verbose_name="Decanato o Division")

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        os.makedirs(settings.MEDIA_ROOT+"/"+self.nombre)
        super(Instancia, self).save(*args, **kwargs)



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
        choices=(('1', 'ene-mar'),
                ('2', 'abr-jul'),
                ('3', 'intensivo'),
                ('4', 'sep-dic')),
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
        verbose_name="contenido sinóptico")
    estrategias_metodologicas                           = models.TextField(
        help_text="Las estratégias metodológicas de enseñanza utilizadas",
        verbose_name="estrategias metodológicas")
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
        if periodo[0] == 'E':
            periodo = "EM"
        elif periodo[0] == 'A':
            periodo = "AJ"
        elif periodo[0] == 'V':
            periodo = "VE"
        else:
            periodo = "SD"
        return "%s/%s-%s-%s.pdf" % (dept, instance.codigo, instance.fecha_año, periodo)
    pdf                                                 = models.FileField(
        upload_to=determinar_lugar,
        help_text="El PDF del programa a analizar",
        verbose_name="pdf")

    def __str__(self):
        """Imprime como '[Código] ([Periodo (dos letras)] [año (0000)])''"""
        return self.codigo + " (" + str(int(self.fecha_periodo)) + " " + str(self.fecha_año) + ")"
    
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
        verbose_name="contenido sinóptico",
        blank=True,
        null=True)
    estrategias_metodologicas                           = models.TextField(
        help_text="Las estratégias metodológicas de enseñanza utilizadas",
        verbose_name="estrategias metodológicas",
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
    texto                                               = models.TextField(
        help_text="El texto extraído del PDF",
        verbose_name="texto extraído",
        blank=True)
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
        return self.codigo + " (" + str(int(self.fecha_periodo)) + " " + str(self.fecha_año) + ")"
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



class TipoCampoAdicional(models.Model):
    """Entidad que mantiene los campos adicionales usados"""

    class Meta:
        verbose_name = "campo adicional"

    nombre                                              = models.CharField(
        max_length=100,
        help_text="El nombre completo del campo adicional",
        verbose_name="nombre")

    def __str__(self):
        """Imprime nombre del campo adicional"""
        return self.nombre

class CampoAdicional(models.Model):
    """ Entidad que mantiene los campos adicionales usados en cada programa """
    class Meta:
        verbose_name = "descripción de campo adicional"

    texto                                               = models.TextField(
        help_text="La descripción del campo adicional",
        verbose_name="descripción",
        blank=True)

    tipo_campo_adicional                                = models.ForeignKey(
        TipoCampoAdicional, on_delete=models.CASCADE,
        help_text="tipo de campo adicional",
        verbose_name="campo adicional",null=True)

    programa_borrador                                   = models.ForeignKey(
        Programa_Borrador, #on_delete=models.CASCADE,
        help_text="El programa asociado",
        verbose_name="programa",null=True)

    programa                                            = models.ForeignKey(
        Programa, #on_delete=models.CASCADE,
        help_text="El programa asociado",
        verbose_name="programa",null=True)


class SeccionFuenteInformacion(models.Model):
    """Seccion de fuente de informacion asociada a un borrador o PASA

    Cada seccion esta asociada a una lista (no vacia) de referencias"""
    class Meta:
        verbose_name = "seccion"
        verbose_name_plural = "secciones"
    subtitulo                                           = models.CharField(
        max_length=100,
        help_text="subtítulo de la sección")

    programa_borrador                                   = models.ForeignKey(
        Programa_Borrador, #on_delete=models.CASCADE,
        help_text="El programa asociado a la seccion",
        verbose_name="programa",null=True)

    programa                                            = models.ForeignKey(
        Programa, #on_delete=models.CASCADE,
        help_text="El programa asociado a la seccion",
        verbose_name="programa",null=True)
    
    def __str__(self):
        return self.subtitulo


class ReferenciaBibliografica(models.Model):
    """Referencias bibliograficas (libros)"""

    class Meta:
        verbose_name = "referencia"
        verbose_name_plural = "referencias"

    titulo                                                  = models.CharField(
        max_length=100,
        help_text="Titulo de la funte recomendada",
        verbose_name="titulo")

    editorial                                               = models.CharField(
        max_length=100,
        help_text="Editorial de la funte recomendada",
        verbose_name="editorial")

    edicion                                                 = models.CharField(
        max_length=100,
        help_text="Edicion o año recomendado",
        verbose_name="edicion")

    notas                                                   = models.CharField(
        max_length=1000,
        help_text="Notas adicionales",
        verbose_name="notas")

    seccion                                                 = models.ForeignKey(
        SeccionFuenteInformacion, on_delete=models.CASCADE,
        help_text="Seccion a la que pertenece la referencia",
        verbose_name="seccion")
    

    def __str__(self):
        """Imprime como un extracto de la referencia"""
        return self.titulo

class AutorReferencia(models.Model):
    """Entidad que representa los autores de una referencia"""
    class Meta:
        verbose_name = "autor"
        verbose_name_plural = "autores"

    nombres                                                 = models.CharField(
        max_length=100,
        verbose_name="nombres")

    apellidos                                               = models.CharField(
        max_length=100,
        verbose_name="apellidos")
