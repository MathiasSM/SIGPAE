from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from .forms import *

# View para subir un nuevo archivo. El resto bloqueado.
def index(request):

    if request.method == 'POST':
        pdf_form = PDFForm(request.POST, request.FILES)
        whole_form = ProgramaForm(request.POST)
        if pdf_form.is_valid():
            instance = pdf_form.save()
            pdf_url = '/media/' + str(instance.pdf.name)
            req = request.POST
            req.appendlist('pdf_url',pdf_url)
            return render(request, 'ocr/extract.html', {'pdf_form': pdf_form, 'pdf_url': pdf_url, 'pdf_texto':instance.texto, 'whole_form': ProgramaForm(req)})
        elif whole_form.is_valid():
            print("PDF not valid. Form is valid.")
            whole_form.save()
            return render(request, 'ocr/archivo.html')
        else:
            print("None valid.")
            messages.error(request, 'El archivo no parece ser un archivo PDF')
            pdf_form = PDFForm()
            return render(request, 'ocr/upload.html', {'pdf_form': pdf_form, 'whole_form': whole_form})

    else:
        pdf_form = PDFForm()
        print("Regular GET")
        return render(request, 'ocr/upload.html', {'pdf_form': pdf_form})

# View del archivo de programas
def archivo(request):
    return render(request, 'ocr/archivo.html')


