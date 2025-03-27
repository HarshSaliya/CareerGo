
from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

from .views import home, process_resume

urlpatterns = [
    path("", home, name="home"),
    path("process_resume/", process_resume, name="process_resume"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
