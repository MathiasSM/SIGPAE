from django.contrib import admin
from ocr.models import *

# Register your models here.
class OrganoAcademicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo')

class UnidadAcademicaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

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
        'estrategias_evaluacion'
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
