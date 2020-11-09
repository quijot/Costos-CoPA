from django.contrib import admin

# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User

from .models import (
    Combustible,
    Empresa,
    GastoEmpresa,
    GastoPersonal,
    Instrumento,
    Profesional,
    TipoGasto,
    Trabajo,
    Vehiculo,
)

admin.site.register(TipoGasto)


class ProfesionalInline(admin.TabularInline):
    model = Profesional
    extra = 0


class VehiculoInline(admin.StackedInline):
    model = Vehiculo
    extra = 0


class InstrumentoInline(admin.TabularInline):
    model = Instrumento
    extra = 0


class GastoEmpresaInline(admin.TabularInline):
    model = GastoEmpresa
    extra = 0


class GastoPersonalInline(admin.TabularInline):
    model = GastoPersonal
    extra = 0


@admin.register(Combustible)
class CombustibleAdmin(admin.ModelAdmin):
    list_display = ["combustible", "valor_litro"]
    # list_filter = []
    # search_fields = []
    # fieldsets = [
    #     (
    #         "Algo",
    #         {
    #             "fields": [
    #                 ("field1", "field2"),
    #                 ("field3", "field4", "field5"),
    #             ],
    #             "classes": ["extrapretty"],
    #         },
    #     )
    # ]
    # search_fields = []
    # readonly_fields = []


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = [
        "nombre",
        "cantidad_de_profesionales",
        "cantidad_de_vehiculos",
        "cantidad_de_instrumentos",
    ]
    list_filter = ["nombre"]
    search_fields = ["nombre"]
    fieldsets = [
        (
            "",
            {
                "fields": [
                    ("nombre"),
                    ("horas_semanales", "gastos_por_hora"),
                    ("cantidad_de_profesionales",),
                    ("cantidad_de_vehiculos",),
                    ("cantidad_de_instrumentos",),
                ],
                "classes": ["extrapretty"],
            },
        )
    ]
    readonly_fields = [
        "gastos_por_hora",
        "cantidad_de_profesionales",
        "cantidad_de_vehiculos",
        "cantidad_de_instrumentos",
    ]
    inlines = [ProfesionalInline, VehiculoInline, InstrumentoInline, GastoEmpresaInline]


@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ["username", "matricula", "last_name", "first_name", "costo_por_hora"]
    # list_filter = []
    # search_fields = []
    # fieldsets = [
    #     (
    #         "Algo",
    #         {
    #             "fields": [
    #                 ("field1", "field2"),
    #                 ("field3", "field4", "field5"),
    #             ],
    #             "classes": ["extrapretty"],
    #         },
    #     )
    # ]
    readonly_fields = ["costo_por_hora"]
    inlines = [GastoPersonalInline]


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "valor_a_nuevo", "kilometraje_anual", "tipo_combustible", "rendimiento", "costo_km"]
    # list_filter = []
    # search_fields = []
    # fieldsets = [
    #     (
    #         "Algo",
    #         {
    #             "fields": [
    #                 ("field1", "field2"),
    #                 ("field3", "field4", "field5"),
    #             ],
    #             "classes": ["extrapretty"],
    #         },
    #     )
    # ]
    # search_fields = []
    readonly_fields = [
        "combustible",
        "valor_residual",
        "amortizacion_valor",
        "kilometraje_mensual",
        "amortizacion_seguro",
        "amortizacion_patente",
        "amortizacion_cochera",
        "amortizacion_lavado",
        "amortizacion_neumaticos",
        "reparaciones",
        "respuestos",
        "service",
        "lubricacion",
        "costo_km",
    ]


@admin.register(Instrumento)
class InstrumentoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "valor_USD", "valor_ARS", "vida_util", "costo_jornada"]
    # list_filter = []
    # search_fields = []
    # fieldsets = [
    #     (
    #         "Algo",
    #         {
    #             "fields": [
    #                 ("field1", "field2"),
    #                 ("field3", "field4", "field5"),
    #             ],
    #             "classes": ["extrapretty"],
    #         },
    #     )
    # ]
    # search_fields = []
    readonly_fields = [
        "valor_ARS",
        "costo_jornada",
    ]


@admin.register(Trabajo)
class TrabajoAdmin(admin.ModelAdmin):
    list_display = ["expediente", "fecha", "comitente", "costo_total"]
    # list_filter = []
    # search_fields = []
    # fieldsets = [
    #     (
    #         "Algo",
    #         {
    #             "fields": [
    #                 ("field1", "field2"),
    #                 ("field3", "field4", "field5"),
    #             ],
    #             "classes": ["extrapretty"],
    #         },
    #     )
    # ]
    filter_horizontal = ["profesionales", "vehiculos", "instrumentos"]
    readonly_fields = [
        "sellado_fiscal",
        "gastos_de_empresa",
        "costo_de_profesionales",
        "movilidad",
        "amortizacion_de_instrumentos",
        "costo_total",
    ]
