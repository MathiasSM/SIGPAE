from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from .forms import *

# View para subir un nuevo archivo. El resto bloqueado.
def index(request):
    pdf_form = PDFForm()

    if request.method == 'POST':
        pdf_form = PDFForm(request.POST, request.FILES)
        whole_form = ProgramaForm(request.POST)
        if pdf_form.is_valid():
            pdf = request.FILES['pdf']
            fs = FileSystemStorage()
            filename = fs.save('tmp/'+pdf.name, pdf)
            pdf_url = fs.url(filename)
            print("PDF is valid")
            return render(request, 'ocr/activado.html', {'pdf_form': PDFForm(), 'pdf_url': pdf_url, 'whole_form': ProgramaForm()})
        elif whole_form.is_valid():
            print("PDF not valid. Form is valid.")
            return render(request, 'ocr/archivo.html')
        else:
            print("None valid.")
            return render(request, 'ocr/bloqueado.html', {'pdf_form': PDFForm()})

    else:
        print("Regular GET")
        return render(request, 'ocr/bloqueado.html', {'pdf_form': pdf_form})

# View del archivo de programas
def archivo(request):
    return render(request, 'ocr/archivo.html')
