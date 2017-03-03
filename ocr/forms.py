from django import forms
from ocr.models import *
from django.core.files.move import file_move_safe
from django.conf import settings

class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('auto_id', '%s')
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'placeholder': field.help_text})


from ocr.pdf2txt.pdf2txt import *
from django.utils.text import get_valid_filename
class PDFForm(BaseModelForm):
    class Meta:
        model = PDFAnonimo
        fields = [ 'pdf', 'tipo', ]

    def save(self, commit=True):
        instance = super(PDFForm, self).save(commit=False)

        if commit:
            instance.save()
            # if self.cleaned_data['tipo']=='I':
            #     instance.texto = convertImgPdf(settings.MEDIA_ROOT+'/'+instance.pdf.name)
            # else:
            #     instance.texto = convertTxtPdf(settings.MEDIA_ROOT+'/'+instance.pdf.name)
            instance.texto = convertImgPdf(settings.MEDIA_ROOT+'/'+instance.pdf.name)
        return instance

class ProgramaForm(BaseModelForm):
    class Meta:
        model = Programa
        exclude = [ 'pdf', ]

    pdf_url = forms.CharField(max_length=100, widget = forms.HiddenInput())

    def save(self, commit=True):
        instance = super(ProgramaForm, self).save(commit=False)

        periodo = instance.fecha_periodo
        if periodo[0] == 'E':   periodo="EM"
        elif periodo[0] == 'A': periodo="AJ"
        elif periodo[0] == 'V': periodo="VE"
        else:                   periodo="SD"

        nurl = "%s/%s-%s-%s.pdf" % (str(instance.instancia), instance.codigo, instance.fecha_año, periodo)

        file_move_safe(settings.BASE_DIR+self.cleaned_data['pdf_url'], settings.MEDIA_ROOT+'/'+nurl, allow_overwrite=True)
        instance.pdf.name = nurl
        if commit:
            instance.save()
        return instance


