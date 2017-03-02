from django.core.exceptions import ValidationError

def validate_pdf_ext_mime(value):
    if not value.name.endswith('.pdf') or value.file.content_type != 'application/pdf':
        raise ValidationError(u'El archivo no parece ser un archivo PDF')