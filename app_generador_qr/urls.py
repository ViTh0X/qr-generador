from django.urls import path
from . import views

urlpatterns = [
    path('', views.generador_qr_index, name='generador_qr_index'),
    path('campos/', views.campos_qr, name='campos_qr'),
    path('generar/', views.generar_qr, name='generar_qr'),
]
