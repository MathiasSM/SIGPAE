from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from .forms import *

# View para subir un nuevo archivo. El resto bloqueado.
def index(request):
    pdf_form = PDFForm()

    if request.method == 'POST':
        if request.FILES['pdf']:
            pdf = request.FILES['pdf']
            fs = FileSystemStorage()
            filename = fs.save(tmp/pdf.name, pdf)
            uploaded_file_url = fs.url(filename)
        elif request.POST['pdf_url']:
            whole_form = ProgramaForm(request.POST)
            if whole_form.is_valid():
                return render(request, 'ocr/archivo.html')

            return render(request, 'ocr/activado.html', {'pdf_url': pdf_url})

    else:
        return render(request, 'ocr/bloqueado.html', {'pdf_form': pdf_form})

# View del archivo de programas
def archivo(request):
    return render(request, 'ocr/archivo.html')
