
from django.contrib import admin
from django.urls import path
from .views import extract_text
urlpatterns = [
    path('admin/', admin.site.urls),
     path('api/extract_text/', extract_text),
]
