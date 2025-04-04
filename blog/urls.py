from django.urls import path
from .views import blog_page

urlpatterns = [
    path('', blog_page, name='blog_list'),
    path('blogs/<slug:slug>/', blog_page, name='blog_detail'),
]
