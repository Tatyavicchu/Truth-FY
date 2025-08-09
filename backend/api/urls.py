from django.urls import path
from . import views

urlpatterns = [
    path('extract_text/', views.extract_text),
    path('analyze_article/', views.analyze_article),
]
