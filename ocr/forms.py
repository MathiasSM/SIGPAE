from django import forms
from ocr.models import *

class PDFForm(forms.Form):
    pdf = forms.FileField(label='PDF')

class ProgramaForm(forms.ModelForm):
    class Meta:
        model = Programa
        exclude = [  ]