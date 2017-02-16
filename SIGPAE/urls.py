"""SIGPAE URL Configuration
"""
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^ocr/', include('ocr.urls')),
    url(r'^admin/', admin.site.urls),
]



from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)