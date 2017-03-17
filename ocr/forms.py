from django import forms
from ocr.models import *
from django.core.files.move import file_move_safe
from django.conf import settings
from django.forms import FileInput, HiddenInput, TextInput
from ocr.pdf2txt.pdf2txt import *
from ocr.pdf2txt.txtlibs import *
from django.utils.text import get_valid_filename

class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('auto_id', '%s')
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'placeholder': field.help_text})


class PDFForm(BaseModelForm):
    class Meta:
        model = PDFAnonimo
        fields = ['pdf', 'tipo']
        widgets = {
            'pdf': FileInput(attrs={'class':'main-upload'}, ),
            'tipo': HiddenInput(),
        }

    def save(self, commit=True):
        instance = super(PDFForm, self).save(commit=False)

        if commit:
            instance.save()
            if self.cleaned_data['tipo'] == 'I':
                instance.texto = convertImgPdf(settings.MEDIA_ROOT+'/'+instance.pdf.name)
            else:
                instance.texto = convertTxtPdf(settings.MEDIA_ROOT+'/'+instance.pdf.name)

        self.instancia_pk, self.codigo_encontrado, self.instancia_nombre = getCode(instance.texto)
        
        print('\n')
        if self.instancia_pk > -1:
            self.instancia_nombre = Instancia.objects.get(pk=self.instancia_pk).nombre

            print("Codigo encontrado, en la tabla y con dependencia asociada:")
            print("Codigo: "+self.codigo_encontrado)
            print("Dependencia: "+self.instancia_nombre)
            
        elif self.instancia_pk == -1:
            print("Codigo encontrado, en la tabla pero sin dependencias asociadas:")
            print("Codigo: "+self.codigo_encontrado)
            print("Instancia: "+self.instancia_nombre)

        elif self.instancia_pk == -2:
            print("Codigo encontrado, pero no en la tabla:")
            print("Codigo: "+self.codigo_encontrado)
        else:
            print("No se encontro codigo")
        
        return instance

class AnonForm(BaseModelForm):
    class Meta:
        model = Programa_Borrador
        exclude = ['pdf', 'texto','published']
        initial = {'horas_laboratorio':0, 'horas_teoria':0, 'horas_practica':0}

    pdf_url = forms.CharField(max_length = 100, widget = forms.HiddenInput())
    pdf_texto = forms.CharField(max_length = 1000000, widget = forms.HiddenInput())

    def save(self, commit=True):
        instance = super(AnonForm, self).save(commit=False)

        periodo = instance.fecha_periodo
        if periodo[0] == 'E':   periodo="EM"
        elif periodo[0] == 'A': periodo="AJ"
        elif periodo[0] == 'V': periodo="VE"
        else:                   periodo="SD"

        nurl = "%s/%s-%s-%s.pdf" % (str(instance.instancia),
                                    instance.codigo,
                                    instance.fecha_año,
                                    periodo)

        file_move_safe(settings.BASE_DIR+self.cleaned_data['pdf_url'],
                       settings.MEDIA_ROOT+'/'+nurl,
                       allow_overwrite=True)
        instance.pdf.name = nurl
        instance.texto = self.cleaned_data['pdf_texto']
        if commit:
            instance.save()
        return instance

class ProgramaForm(BaseModelForm):
    class Meta:
        model = Programa_Borrador
        exclude = ['pdf', 'texto','published']
        widgets = {'codigo': TextInput(attrs={'maxlength': '7'},),}

    def save(self, commit=True):
        instance = super(ProgramaForm, self).save(commit=False)

        if commit:
            instance.save()
        return instance
