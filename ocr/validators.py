"""Validadores custom para la aplicación OCR."""

from django.core.exceptions import ValidationError

def validate_pdf_ext_mime(value):
    """Valida el archivo por extensión y por MIME type."""

    if not value.name.endswith('.pdf') or value.file.content_type != 'application/pdf':
        raise ValidationError('El archivo no parece ser un archivo PDF')
