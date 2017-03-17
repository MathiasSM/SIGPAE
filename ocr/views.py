"""Vistas de control del sistema SIGPAE-Históricos"""

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Programa_Borrador
from .forms import PDFForm, ProgramaForm, AnonForm, Instancia

from django.db import connections
from collections import namedtuple

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def index(request):
    """Vista principal del sistema SIGPAE-Histórico"""

    cursor = connections['SIGPAEdb'].cursor()
    cursor.execute("SELECT b1.clave as b1clave, b2.clave as b2clave FROM test as b1, test as b2")
    row = namedtuplefetchall(cursor)
    #row = cursor.fetchall()

    print(row)

    if request.method == 'POST':
        print('POST:')
        print(request.POST)
        print('FILES:')
        print(request.FILES)
        print()
        if request.FILES is {}:
            print("Got a 'POST without PDF'")
            messages.error(request, 'No has seleccionado algún archivo')
            pdf_form = PDFForm(initial={'tipo': 'T'})
            borradores = Programa_Borrador.objects.all()
            return render(request, 'ocr/index.html', {'form': pdf_form, 'borradores':borradores})
        vista_editar = try_edit(request)
        if vista_editar is not None:
            return vista_editar
        else:
            print("Got a 'POST with invalid PDF'")
            messages.error(request, 'El archivo no parece ser un PDF')
            pdf_form = PDFForm(initial={'tipo': 'T'})
            borradores = Programa_Borrador.objects.all()
            return render(request, 'ocr/index.html', {'form': pdf_form, 'borradores':borradores})
    else: # if request.method == 'GET'
        pdf_form = PDFForm(initial={'tipo': 'T'})
        print("Got a 'GET'")
        borradores = Programa_Borrador.objects.all()
        return render(request, 'ocr/index.html', {'form': pdf_form, 'borradores':borradores})

def try_edit(request):
    """Vista intermedia/falsa para la generación de html para edición de programa anónimo"""
    print(request.POST)
    form = PDFForm(request.POST, request.FILES)
    if form.is_valid():
        instance = form.save()
        pdf_url = '/media/' + str(instance.pdf.name)
        pdf_texto = instance.texto
        req = request.POST
        req.appendlist('pdf_url', pdf_url)
        req.appendlist('pdf_texto', pdf_texto)
        instS, cod = form.instancia_nombre, form.codigo_encontrado
        instS = Instancia.objects.values_list('pk', flat=True).get(nombre=instS)
        form = AnonForm(initial={'pdf_url': pdf_url,
                                 'pdf_texto': pdf_texto,
                                 'instancia': instS,
                                 'codigo': cod})
        print(instS)
        return render(request, 'ocr/editar_anon.html',
                      {'pdf_url': pdf_url,
                       'pdf_texto':pdf_texto,
                       'form': form})
    return None

def try_keep(request):
    """Vista para subir info del PDF anónimo"""
    if request.method == 'POST':
        print(request.POST)
        form = AnonForm(request.POST)
        if form.is_valid():
            instance = form.save()
            messages.success(request, 'Se ha guardado el borrador #%s con éxito!' % instance.pk)
            return redirect('ocr:borradores')

        messages.error(request, 'No se ha guardado el borrador')
        return render(request, 'ocr/editar_anon.html',
                      {'form': AnonForm(request.POST)})
    return redirect('ocr:index')


def editar_borrador(request, draft_id):
    """Vista de edición de un borrador"""
    try:
        borrador = Programa_Borrador.objects.get(pk=draft_id)
        if request.method == 'POST':
            form = ProgramaForm(request.POST, instance=borrador)
            print(request.POST)
            if form.is_valid():
                instance = form.save()
                messages.success(request, 'Se han guardado cambios al borrador #%s!' % instance.pk)
                return render(request, 'ocr/editar_borrador.html',
                              {'pdf_url': '/media/%s' % str(borrador.pdf),
                               'pdf_texto': borrador.texto,
                               'form': form})
            else:
                messages.error(request, 'Hubo un error al guardar los cambios')
                return render(request, 'ocr/editar_borrador.html',
                              {'pdf_url': '/media/%s' % str(borrador.pdf),
                               'pdf_texto': borrador.texto,
                               'form': form})
        else:
            form = ProgramaForm(instance=borrador)
            return render(request, 'ocr/editar_borrador.html',
                          {'pdf_url': '/media/%s' % str(borrador.pdf),
                           'pdf_texto': borrador.texto,
                           'form': form})
    except Programa_Borrador.DoesNotExist:
        return render(request, 'ocr/borrador_404.html', status=404, context={'draft_id': draft_id})


def listar_borradores(request):
    """Vista de todos los borradores almacenados en el sistema"""
    borradores = Programa_Borrador.objects.all()
    return render(request, 'ocr/archivo.html', {'borradores':borradores})
