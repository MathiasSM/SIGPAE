from django import forms
from ocr.models import *

class PDFForm(forms.Form):
    pdf = FileField()

class ProgramaForm(forms.ModelForm):
    class Meta:
        model = Programa
        exclude = [  ]