from django.contrib import admin
from ocr.models import *

# Register your models here.

class InstanciaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

class ProgramaAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'fecha_periodo',
        'fecha_año',
        'instancia'
    )
    fields = (
        ('codigo', 'creditos'),
        'instancia',
        'denominacion',
        ('fecha_periodo', 'fecha_año'),
        ('horas_teoria', 'horas_practica', 'horas_laboratorio'),
        'objetivos',
        'contenidos_sinopticos',
        'estrategias_metodologicas',
        'estrategias_evaluacion',
        'pdf'
    )

class PDFAnonimoAdmin(admin.ModelAdmin):
    def view_link(self, obj):
        return u"<a href='%d/'>View</a>" % obj.id
    view_link.short_description = ''
    view_link.allow_tags = True

    list_display = (
        'pdf',
        'tipo',
        'view_link'
    )
    fields = (
        ('pdf', 'tipo'),
        'texto'
    )


class ReferenciaBibliograficaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'programa')




admin.site.register(Instancia, InstanciaAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(PDFAnonimo, PDFAnonimoAdmin)
admin.site.register(ReferenciaBibliografica, ReferenciaBibliograficaAdmin)
