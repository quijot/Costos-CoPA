import decimal

from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import DecimalPreference
from dynamic_preferences.users.registries import user_preferences_registry

# Sections
# --------
combustible = Section("combustible")
trabajo = Section("trabajo", verbose_name="Preferencias de Trabajo")


# Global Preferences
# ------------------
@global_preferences_registry.register
class CotizacionDolar(DecimalPreference):
    name = "cotizacion_dolar"
    default = decimal.Decimal(80)
    required = True


@global_preferences_registry.register
class ModuloTributario(DecimalPreference):
    name = "modulo_tributario"
    default = decimal.Decimal(0.75)
    required = True


@global_preferences_registry.register
class Nafta(DecimalPreference):
    name = "nafta"
    section = combustible
    default = decimal.Decimal(1)
    required = True


@global_preferences_registry.register
class NaftaPremium(DecimalPreference):
    name = "nafta_premium"
    section = combustible
    default = decimal.Decimal(1)
    required = True


@global_preferences_registry.register
class Diesel(DecimalPreference):
    name = "diesel"
    section = combustible
    default = decimal.Decimal(1)
    required = True


@global_preferences_registry.register
class DieselPremium(DecimalPreference):
    name = "diesel_premium"
    section = combustible
    default = decimal.Decimal(1)
    required = True


@global_preferences_registry.register
class GNC(DecimalPreference):
    name = "gnc"
    section = combustible
    default = decimal.Decimal(1)
    required = True


# User Preferences
# ----------------
@user_preferences_registry.register
class Visados(DecimalPreference):
    section = trabajo
    name = "visados"
    verbose_name = "Monto por visados"
    help_text = "Gastos en reparticiones públicas."
    default = decimal.Decimal(0)


@user_preferences_registry.register
class Ayudante(DecimalPreference):
    section = trabajo
    name = "ayudante"
    verbose_name = "Ayudante"
    help_text = "Pago de jornales a ayudante/s."
    default = decimal.Decimal(0)


@user_preferences_registry.register
class Viaticos(DecimalPreference):
    section = trabajo
    name = "viaticos"
    verbose_name = "Viáticos"
    help_text = "Pago de alojamiento / comidas."
    default = decimal.Decimal(0)


@user_preferences_registry.register
class Mojones(DecimalPreference):
    section = trabajo
    name = "mojones"
    verbose_name = "Mojones"
    help_text = "Gasto en hierros, estacas, pintura, cintas peligro."
    default = decimal.Decimal(0)


@user_preferences_registry.register
class AlquilerInstrumentos(DecimalPreference):
    section = trabajo
    name = "alquiler_instrumentos"
    verbose_name = "Alquiler instrumentos"
    help_text = "Pago de alquileres ocasionales para este trabajo."
    default = decimal.Decimal(0)


@user_preferences_registry.register
class SegurosEspeciales(DecimalPreference):
    section = trabajo
    name = "seguros_especiales"
    verbose_name = "Seguros especiales"
    help_text = "Pago de seguros ocasionales para este trabajo."
    default = decimal.Decimal(0)


@user_preferences_registry.register
class Dibujante(DecimalPreference):
    section = trabajo
    name = "dibujante"
    verbose_name = "Dibujante"
    help_text = "Pago a dibujante/s."
    default = decimal.Decimal(0)


@user_preferences_registry.register
class Impresiones(DecimalPreference):
    section = trabajo
    name = "impresiones"
    verbose_name = "Impresiones / ploteos"
    help_text = "Pago por ploteos / impresiones de documentación."
    default = decimal.Decimal(0)


@user_preferences_registry.register
class Gestor(DecimalPreference):
    section = trabajo
    name = "gestor"
    verbose_name = "Gestor / Comisionista"
    help_text = "Pago a gestores, comisionistas, fletes."
    default = decimal.Decimal(0)


@user_preferences_registry.register
class OtrosGastos(DecimalPreference):
    section = trabajo
    name = "otros_gastos"
    verbose_name = "Otros gastos"
    help_text = "Otros gastos sin categorizar."
    default = decimal.Decimal(0)


# Helpers
# -------
def global_parameters(section, name):
    global_preferences = global_preferences_registry.manager()
    param = f"{section}__{name}" if section else name
    return global_preferences[param]


def get_cotizacion_dolar():
    return global_parameters(None, "cotizacion_dolar")


def get_modulo_tributario():
    return global_parameters(None, "modulo_tributario")


def get_valor_litro(tipo_combustible):
    tipo = tipo_combustible.lower().replace(" ", "_")
    return global_parameters(combustible, tipo)
