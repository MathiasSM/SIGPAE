"""Vistas de control del sistema SIGPAE-Históricos"""

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import PDFForm, ProgramaForm, AnonForm, Instancia, Decanato

def index(request):
    """Vista principal del sistema SIGPAE-Histórico"""
    if request.method == 'POST':
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

def get_instancias_ordenaditas():
    """Esto NO es una vista. Función helper para el dropdown de selección de instancia."""
    secs = Decanato.objects.values_list('pk', 'nombre').order_by('nombre')
    dic = {}
    for pk, no in secs:
        insL = []
        insQ = Instancia.objects.values_list('pk', 'nombre').filter(decanato=pk).order_by('nombre')
        for i_pk, i_no in insQ:
            insL += [(i_pk, i_no),]
        dic.update({no: insL})
    return dic

INSTANCIAS = get_instancias_ordenaditas()


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
        print(pdf_url)
        instPK, instS, cod = form.instancia_pk, form.instancia_nombre, form.codigo_encontrado
        if(instPK>-1):
            instS = Instancia.objects.values_list('pk', flat=True).get(nombre=instS)
            form = AnonForm(initial={'pdf_url': pdf_url,
                                     'pdf_texto': pdf_texto,
                                     'codigo': cod})
        elif(instPK==-1):
            form = AnonForm(initial={'pdf_url': pdf_url,
                                     'pdf_texto': pdf_texto,
                                     'codigo': cod})
        else:
            form = AnonForm(initial={'pdf_url': pdf_url,
                                     'pdf_texto': pdf_texto,
                                     'codigo': ''})
        return render(request, 'ocr/editar_anon.html',
                      {'pdf_url': pdf_url,
                       'pdf_texto':pdf_texto,
                       'form': form,
                       'selectI': INSTANCIAS,
                       'instancia': instS})
    return None

def try_keep(request):
    """Vista para subir info del PDF anónimo"""
    if request.method == 'POST':
        form = AnonForm(request.POST)
        a = Instancia.objects.values_list('pk',flat=True).get(pk=request.POST['instancia'])
        
        
        
        if form.is_valid():
            instance = form.save()
            # GUARDAR CAMPOS EXTRAS
            n_extra = 0
            iterador_tipos = 'tipo1'
            iterador_valores = 'valor1'
            iterador_pkvalores = 'pkvalor1'
            cur_tipo = request.POST.get(iterador_tipos,False)
            cur_valor = request.POST.get(iterador_valores,False)
            cur_pkvalor = request.POST.get(iterador_pkvalores,False)
            while(cur_pkvalor):
                cur_pkvalor = int(cur_pkvalor)
                n_extra+=1
                if(cur_tipo != '' or cur_valor != ''):
                    if(not TipoCampoAdicional.objects.filter(nombre=cur_tipo).exists()):
                        este_tipo = TipoCampoAdicional(nombre=cur_tipo)
                        este_tipo.save()
                    else:
                        este_tipo = TipoCampoAdicional.objects.get(nombre=cur_tipo)
                    este_valor = CampoAdicional(texto=cur_valor,
                                                tipo_campo_adicional=este_tipo,
                                                programa_borrador=instance)
                    este_valor.save()
                
                iterador_tipos = 'tipo%s' % (n_extra+1)
                iterador_valores = 'valor%s' % (n_extra+1)
                cur_tipo = request.POST.get(iterador_tipos,False)
                cur_valor = request.POST.get(iterador_valores,False)
            # / GUARDAR CAMPOS EXTRAS

            # GUARDAR LAS SECCIONES DE LAS REFERENCIAS
            seccion_cnt = 1
            iterador_seccion_nombre = 'seccionNombre%s' % (seccion_cnt)
            iterador_seccion_pk = 'seccionpk%s' % (seccion_cnt)
            cur_seccion_nombre = request.POST.get(iterador_seccion_nombre,False)
            cur_seccion_pk = request.POST.get(iterador_seccion_pk,False)
            while(cur_seccion_pk):
                cur_seccion_pk = int(cur_seccion_pk)
                esta_seccion = SeccionFuenteInformacion(subtitulo=cur_seccion_nombre,programa_borrador=instance)
                esta_seccion.save()

                # GUARDAR LAS REFERENCIAS DE LA SECCION
                referencia_cnt = 1
                iterador_referencia_titulo = 'titulo%s-%s' % (seccion_cnt, referencia_cnt)
                iterador_referencia_editorial = 'editorial%s-%s' % (seccion_cnt, referencia_cnt)
                iterador_referencia_edicion = 'edicion%s-%s' % (seccion_cnt, referencia_cnt)
                iterador_referencia_notas = 'notas%s-%s' % (seccion_cnt, referencia_cnt)
                iterador_referencia_pk = 'referenciapk%s-%s' % (seccion_cnt, referencia_cnt)
                cur_referencia_titulo = request.POST.get(iterador_referencia_titulo,False)
                cur_referencia_editorial = request.POST.get(iterador_referencia_editorial,False)
                cur_referencia_edicion = request.POST.get(iterador_referencia_edicion,False)
                cur_referencia_notas = request.POST.get(iterador_referencia_notas,False)
                cur_referencia_pk = request.POST.get(iterador_referencia_pk,False)
                while(cur_referencia_pk):
                    cur_referencia_pk = int (cur_referencia_pk)
                    esta_referencia = ReferenciaBibliografica(titulo=cur_referencia_titulo,
                                                    editorial=cur_referencia_editorial,
                                                    edicion=cur_referencia_edicion,
                                                    notas=cur_referencia_notas,
                                                    seccion=esta_seccion)
                    esta_referencia.save()

                    # GUARDAR LOS AUTORES PARA ESTA REFERENCIA
                    autor_cnt = 1
                    iterador_autor_nombres = 'nombres%s-%s-%s' % (seccion_cnt, referencia_cnt, autor_cnt)
                    iterador_autor_apellidos = 'nombres%s-%s-%s' % (seccion_cnt, referencia_cnt, autor_cnt)
                    iterador_autor_pk = 'autorpk%s-%s-%s' % (seccion_cnt, referencia_cnt, autor_cnt)
                    cur_autor_nombres = request.POST.get(iterador_autor_nombres,False)
                    cur_autor_apellidos = request.POST.get(iterador_autor_apellidos,False)
                    cur_autor_pk = request.POST.get(iterador_autor_pk,False)
                    while(cur_autor_nombres):
                        este_autor = AutorReferencia(nombres=cur_autor_nombres,
                                                    apellidos=cur_autor_apellidos,
                                                    referencia=esta_referencia)
                        este_autor.save()
                        autor_cnt += 1
                        iterador_autor_nombres = 'nombres%s-%s-%s' % (seccion_cnt, referencia_cnt, autor_cnt)
                        iterador_autor_apellidos = 'nombres%s-%s-%s' % (seccion_cnt, referencia_cnt, autor_cnt)
                        iterador_autor_pk = 'autorpk%s-%s-%s' % (seccion_cnt, referencia_cnt, autor_cnt)
                        cur_autor_nombres = request.POST.get(iterador_autor_nombres,False)
                        cur_autor_apellidos = request.POST.get(iterador_autor_apellidos,False)
                        cur_autor_pk = request.POST.get(iterador_autor_pk,False)
                    # / GUARDAR LOS AUTORES PARA ESTA REFERENCIA

                    referencia_cnt += 1
                    iterador_referencia_titulo = 'titulo%s-%s' % (seccion_cnt, referencia_cnt)
                    iterador_referencia_editorial = 'editorial%s-%s' % (seccion_cnt, referencia_cnt)
                    iterador_referencia_edicion = 'edicion%s-%s' % (seccion_cnt, referencia_cnt)
                    iterador_referencia_notas = 'notas%s-%s' % (seccion_cnt, referencia_cnt)
                    iterador_referencia_pk = 'referenciapk%s-%s' % (seccion_cnt, referencia_cnt)
                    cur_referencia_titulo = request.POST.get(iterador_referencia_titulo,False)
                    cur_referencia_editorial = request.POST.get(iterador_referencia_editorial,False)
                    cur_referencia_edicion = request.POST.get(iterador_referencia_edicion,False)
                    cur_referencia_notas = request.POST.get(iterador_referencia_notas,False)
                    cur_referencia_pk = request.POST.get(iterador_referencia_pk,False)
                # / GUARDAR LAS REFERENCIAS DE LA SECCION

                seccion_cnt += 1
                iterador_seccion_nombre = 'seccionNombre%s' % (seccion_cnt)
                iterador_seccion_pk = 'seccionpk%s' % (seccion_cnt)
                cur_seccion_nombre = request.POST.get(iterador_seccion_nombre,False)
                cur_seccion_pk = request.POST.get(iterador_seccion_pk,False)
            # / GUARDAR LAS SECCIONES DE LAS REFERENCIAS
            
            messages.success(request, 'Se ha guardado el borrador #%s con éxito!' % instance.pk)
            #print(request.POST['pdf_texto'])
            print(str(instance.pdf))
            return redirect('ocr:borradores')

        messages.error(request, 'No se ha guardado el borrador')
        return render(request, 'ocr/editar_anon.html',
                      {'form': form,
                      'selectI': INSTANCIAS,
                      'instancia': a,
                      'pdf_texto': request.POST['pdf_texto'],
                      'pdf_url': request.POST['pdf_url']})
    return redirect('ocr:index')


def editar_borrador(request, draft_id):
    """Vista de edición de un borrador"""
    try:
        borrador = Programa_Borrador.objects.get(pk=draft_id)
        campos_extra = CampoAdicional.objects.filter(programa_borrador=borrador)
        secciones = SeccionFuenteInformacion.objects.filter(programa_borrador=borrador)
        if request.method == 'POST':
            form = ProgramaForm(request.POST, instance=borrador)
            a = Instancia.objects.values_list('pk',flat=True).get(pk=request.POST['instancia'])
            #print(request.POST)
            if form.is_valid():
                instance = form.save()
                # GUARDAR CAMPOS EXTRAS
                n_extra = 0
                iterador_tipos = 'tipo1'
                iterador_valores = 'valor1'
                iterador_pkvalores = 'pkvalor1'
                cur_tipo = request.POST.get(iterador_tipos,False)
                cur_valor = request.POST.get(iterador_valores,False)
                cur_pkvalor = request.POST.get(iterador_pkvalores,False)
                while(cur_pkvalor):
                    cur_pkvalor = int(cur_pkvalor)
                    n_extra+=1
                    if(not TipoCampoAdicional.objects.filter(nombre=cur_tipo).exists()):
                        este_tipo = TipoCampoAdicional(nombre=cur_tipo)
                        este_tipo.save()
                    else:
                        este_tipo = TipoCampoAdicional.objects.get(nombre=cur_tipo)

                    if(cur_pkvalor == -1):
                        este_valor = CampoAdicional(texto=cur_valor,
                                                tipo_campo_adicional=este_tipo,
                                                programa_borrador=instance)
                    else:
                        este_valor = CampoAdicional.objects.get(pk=cur_pkvalor)
                        este_valor.texto = cur_valor
                        este_valor.tipo_campo_adicional=este_tipo

                    este_valor.save()

                    if(cur_tipo == '' and cur_valor == ''):
                        este_valor.delete()
                    
                    iterador_tipos = 'tipo%s' % (n_extra+1)
                    iterador_valores = 'valor%s' % (n_extra+1)
                    iterador_pkvalores = 'pkvalor%s' % (n_extra+1)
                    cur_tipo = request.POST.get(iterador_tipos,False)
                    cur_valor = request.POST.get(iterador_valores,False)
                    cur_pkvalor = request.POST.get(iterador_pkvalores,False)
                # / GUARDAR CAMPOS EXTRAS

                # GUARDAR LAS SECCIONES DE LAS REFERENCIAS
                seccion_cnt = 1
                iterador_seccion_nombre = 'seccionNombre%s' % (seccion_cnt)
                iterador_seccion_pk = 'seccionpk%s' % (seccion_cnt)
                cur_seccion_nombre = request.POST.get(iterador_seccion_nombre,False)
                cur_seccion_pk = request.POST.get(iterador_seccion_pk,False)
                while(cur_seccion_pk):
                    print(cur_seccion_pk)
                    cur_seccion_pk = int(cur_seccion_pk)
                    esta_seccion = SeccionFuenteInformacion(subtitulo=cur_seccion_nombre,programa_borrador=instance)
                    esta_seccion.save()

                    # GUARDAR LAS REFERENCIAS DE LA SECCION
                    referencia_cnt = 1
                    iterador_referencia_titulo = 'titulo%s-%s' % (seccion_cnt, referencia_cnt)
                    iterador_referencia_editorial = 'editorial%s-%s' % (seccion_cnt, referencia_cnt)
                    iterador_referencia_edicion = 'edicion%s-%s' % (seccion_cnt, referencia_cnt)
                    iterador_referencia_notas = 'notas%s-%s' % (seccion_cnt, referencia_cnt)
                    iterador_referencia_pk = 'referenciapk%s-%s' % (seccion_cnt, referencia_cnt)
                    cur_referencia_titulo = request.POST.get(iterador_referencia_titulo,False)
                    cur_referencia_editorial = request.POST.get(iterador_referencia_editorial,False)
                    cur_referencia_edicion = request.POST.get(iterador_referencia_edicion,False)
                    cur_referencia_notas = request.POST.get(iterador_referencia_notas,False)
                    cur_referencia_pk = request.POST.get(iterador_referencia_pk,False)
                    while(cur_referencia_pk):
                        cur_referencia_pk = int (cur_referencia_pk)
                        esta_referencia = ReferenciaBibliografica(titulo=cur_referencia_titulo,
                                                        editorial=cur_referencia_editorial,
                                                        edicion=cur_referencia_edicion,
                                                        notas=cur_referencia_notas,
                                                        seccion=esta_seccion)
                        esta_referencia.save()

                        # GUARDAR LOS AUTORES PARA ESTA REFERENCIA
                        autor_cnt = 1
                        iterador_autor_nombres = 'nombres%s-%s-%s' % (seccion_cnt, referencia_cnt, autor_cnt)
                        iterador_autor_apellidos = 'nombres%s-%s-%s' % (seccion_cnt, referencia_cnt, autor_cnt)
                        iterador_autor_pk = 'autorpk%s-%s-%s' % (seccion_cnt, referencia_cnt, autor_cnt)
                        cur_autor_nombres = request.POST.get(iterador_autor_nombres,False)
                        cur_autor_apellidos = request.POST.get(iterador_autor_apellidos,False)
                        cur_autor_pk = request.POST.get(iterador_autor_pk,False)
                        while(cur_autor_nombres):
                            este_autor = AutorReferencia(nombres=cur_autor_nombres,
                                                        apellidos=cur_autor_apellidos,
                                                        referencia=esta_referencia)
                            autor_cnt += 1
                            iterador_autor_nombres = 'nombres%s-%s-%s' % (seccion_cnt, referencia_cnt, autor_cnt)
                            iterador_autor_apellidos = 'nombres%s-%s-%s' % (seccion_cnt, referencia_cnt, autor_cnt)
                            iterador_autor_pk = 'autorpk%s-%s-%s' % (seccion_cnt, referencia_cnt, autor_cnt)
                            cur_autor_nombres = request.POST.get(iterador_autor_nombres,False)
                            cur_autor_apellidos = request.POST.get(iterador_autor_apellidos,False)
                            cur_autor_pk = request.POST.get(iterador_autor_pk,False)
                        # / GUARDAR LOS AUTORES PARA ESTA REFERENCIA

                        referencia_cnt += 1
                        iterador_referencia_titulo = 'titulo%s-%s' % (seccion_cnt, referencia_cnt)
                        iterador_referencia_editorial = 'editorial%s-%s' % (seccion_cnt, referencia_cnt)
                        iterador_referencia_edicion = 'edicion%s-%s' % (seccion_cnt, referencia_cnt)
                        iterador_referencia_notas = 'notas%s-%s' % (seccion_cnt, referencia_cnt)
                        iterador_referencia_pk = 'referenciapk%s-%s' % (seccion_cnt, referencia_cnt)
                        cur_referencia_titulo = request.POST.get(iterador_referencia_titulo,False)
                        cur_referencia_editorial = request.POST.get(iterador_referencia_editorial,False)
                        cur_referencia_edicion = request.POST.get(iterador_referencia_edicion,False)
                        cur_referencia_notas = request.POST.get(iterador_referencia_notas,False)
                        cur_referencia_pk = request.POST.get(iterador_referencia_pk,False)
                    # / GUARDAR LAS REFERENCIAS DE LA SECCION

                    seccion_cnt += 1
                    iterador_seccion_nombre = 'seccionNombre%s' % (seccion_cnt)
                    iterador_seccion_pk = 'seccionpk%s' % (seccion_cnt)
                    cur_seccion_nombre = request.POST.get(iterador_seccion_nombre,False)
                    cur_seccion_pk = request.POST.get(iterador_seccion_pk,False)
                # / GUARDAR LAS SECCIONES DE LAS REFERENCIAS


                messages.success(request, 'Se han guardado cambios al borrador #%s!' % instance.pk)
                return render(request, 'ocr/editar_borrador.html',
                              {'pdf_url': '/media/%s' % str(borrador.pdf.name),
                               'pdf_texto': borrador.texto,
                               'form': form,
                               'selectI': INSTANCIAS,
                               'instancia': a,
                               'extras': campos_extra,
                               'secciones': secciones})
            else:
                messages.error(request, 'Hubo un error al guardar los cambios')
                return render(request, 'ocr/editar_borrador.html',
                              {'pdf_url': '/media/%s' % str(borrador.pdf.name),
                               'pdf_texto': borrador.texto,
                               'form': form,
                               'selectI': INSTANCIAS,
                               'instancia': a,
                               'extras': campos_extra,
                               'secciones': secciones})
        else:
            form = ProgramaForm(instance=borrador)
            return render(request, 'ocr/editar_borrador.html',
                          {'pdf_url': '/media/%s' % str(borrador.pdf.name),
                            'pdf_texto': borrador.texto,
                            'form': form,
                            'selectI': INSTANCIAS,
                            'instancia': Instancia.objects.values_list('pk',flat=True).get(pk=draft_id),
                            'extras': campos_extra,
                            'secciones': secciones})
    except Programa_Borrador.DoesNotExist:
        return render(request, 'ocr/borrador_404.html', status=404, context={'draft_id': draft_id})


def listar_borradores(request):
    """Vista de todos los borradores almacenados en el sistema"""
    borradores = Programa_Borrador.objects.all()
    return render(request, 'ocr/archivo.html', {'borradores':borradores})
    


def buscar_publicados(request, codigo, año=9999, periodo=3):
    """Vista de busqueda de PAs"""
    programas = Programa_Borrador.objects.filter(published=True).filter(codigo=codigo).filter(fecha_año__lt=año+1)
    telotengo = Programa_Borrador.objects.filter(published=True).filter(codigo=codigo).filter(fecha_año=año).filter(fecha_periodo=periodo)
    if telotengo:
        pass
        # ir de una al de sacar de este programa un borrador
    if programas:
        return render(request, 'ocr/archivo.html', context={'programas': programas})
    else:
        return render(request, 'ocr/archivo.html')
