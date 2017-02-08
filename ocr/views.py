from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'ocr/index.html')

def archivo(request):
    return render(request, 'ocr/archivo.html')
