from django.contrib import admin
from ocr.models import *

# Register your models here.

class AdscritoAInline(admin.TabularInline):
    model = UnidadAcademica.organo.through
    extra = 1
    verbose_name = "pertenencia de Unidad a Organo Académico"

class OrganoAcademicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo')
    inlines = [AdscritoAInline,]

class UnidadAcademicaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    inlines = [AdscritoAInline,]
    exclude = ('organo',)

class ProgramaAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'fecha_periodo',
        'fecha_año',
        'departamento'
    )
    fields = (
        ('codigo', 'creditos'),
        'departamento',
        'denominacion',
        ('fecha_periodo', 'fecha_año'),
        ('horas_teoria', 'horas_practica', 'horas_laboratorio'),
        'objetivos',
        'contenidos_sinopticos',
        'estrategias_metodologicas',
        'estrategias_evaluacion',
        'pdf'
    )

class RequisitoAdmin(admin.ModelAdmin):
    list_display = ('texto', 'programa')

class ReferenciaBibliograficaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'programa')




admin.site.register(OrganoAcademico, OrganoAcademicoAdmin)
admin.site.register(UnidadAcademica, UnidadAcademicaAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(Requisito, RequisitoAdmin)
admin.site.register(ReferenciaBibliografica, ReferenciaBibliograficaAdmin)
