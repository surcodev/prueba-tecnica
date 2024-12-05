from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('panel_cliente/', views.panel_cliente, name='panel_cliente'),
    path('panel_agente/', views.panel_agente, name='panel_agente'),
    path('panel_admin/', views.panel_admin, name='panel_admin'),
    path('logout/', views.logout_view, name='logout'),
    path('crear_cita/', views.crear_cita, name='crear_cita'),
    path('actualizar_estado_cita/', views.actualizar_estado_cita, name='actualizar_estado_cita'),
    path('asignar-agente/', views.asignar_agente, name='asignar_agente'),
    path('registro_cliente/', views.registro_cliente, name='registro_cliente'),
    path('registro-agente/', views.registro_agente, name='registro_agente'),


]
