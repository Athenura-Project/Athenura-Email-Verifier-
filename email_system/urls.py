from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from email_system import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('email_verifier.urls')),
    path('', include('bulk_sender.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)