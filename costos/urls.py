from django.urls import include, path
from rest_framework import routers

from . import views

# REST Framework
router = routers.DefaultRouter()

urlpatterns = (
    # Inicio
    path("", views.Home.as_view(), name="index"),
    # REST Framework
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/v1/", include(router.urls)),
    # Empresas
    path("empresa/detail/<int:pk>/", views.EmpresaDetailView.as_view(), name="empresa_detail"),
    path("empresa/create/", views.EmpresaCreateView.as_view(), name="empresa_create"),
    path("empresa/update/<int:pk>/", views.EmpresaUpdateView.as_view(), name="empresa_update"),
    # Profesionales
    path("profesionales/", views.ProfesionalListView.as_view(), name="profesional_list"),
    path("profesional/detail/<int:pk>/", views.ProfesionalDetailView.as_view(), name="profesional_detail"),
    path("profesional/preferences/<str:section>", views.user_preferences, name="profesional_preferences"),
    path("profesional/update/<int:pk>/", views.ProfesionalUpdateView.as_view(), name="profesional_update"),
    # Instrumentos
    path("instrumentos/", views.InstrumentoListView.as_view(), name="instrumento_list"),
    path("instrumento/create/", views.InstrumentoCreateView.as_view(), name="instrumento_create"),
    path("instrumento/detail/<int:pk>/", views.InstrumentoDetailView.as_view(), name="instrumento_detail"),
    path("instrumento/update/<int:pk>/", views.InstrumentoUpdateView.as_view(), name="instrumento_update"),
    path("instrumento/delete/<int:pk>/", views.InstrumentoDeleteView.as_view(), name="instrumento_delete"),
    # Vehículos
    path("vehiculos/", views.VehiculoListView.as_view(), name="vehiculo_list"),
    path("vehiculo/create/", views.VehiculoCreateView.as_view(), name="vehiculo_create"),
    path("vehiculo/detail/<int:pk>/", views.VehiculoDetailView.as_view(), name="vehiculo_detail"),
    path("vehiculo/update/<int:pk>/", views.VehiculoUpdateView.as_view(), name="vehiculo_update"),
    path("vehiculo/delete/<int:pk>/", views.VehiculoDeleteView.as_view(), name="vehiculo_delete"),
    # Trabajos
    path("trabajos/", views.TrabajoListView.as_view(), name="trabajo_list"),
    path("trabajo/create/", views.TrabajoCreateView.as_view(), name="trabajo_create"),
    path("trabajo/detail/<int:pk>/", views.TrabajoDetailView.as_view(), name="trabajo_detail"),
    path("trabajo/update/<int:pk>/", views.TrabajoUpdateView.as_view(), name="trabajo_update"),
    path("trabajo/delete/<int:pk>/", views.TrabajoDeleteView.as_view(), name="trabajo_delete"),
)
