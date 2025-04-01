
from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

from .views import home, process_resume , plan_list , payment_page , process_payment


urlpatterns = [
    path("", home, name="home"),
    path("process_resume/", process_resume, name="process_resume"),
    path("plans/", plan_list, name="plan_list"),
    path("payment/<int:plan_id>/", payment_page, name="payment_page"),
    path("process_payment/", process_payment, name="process_payment"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
