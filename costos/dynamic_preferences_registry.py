import decimal

from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import DecimalPreference

# we create some section objects to link related preferences together

general = Section("general")
general = Section("combustible")


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
    section = "combustible"
    default = decimal.Decimal(1)
    required = True


@global_preferences_registry.register
class NaftaPremium(DecimalPreference):
    name = "nafta_premium"
    section = "combustible"
    default = decimal.Decimal(1)
    required = True


@global_preferences_registry.register
class Diesel(DecimalPreference):
    name = "diesel"
    section = "combustible"
    default = decimal.Decimal(1)
    required = True


@global_preferences_registry.register
class DieselPremium(DecimalPreference):
    name = "diesel_premium"
    section = "combustible"
    default = decimal.Decimal(1)
    required = True


@global_preferences_registry.register
class GNC(DecimalPreference):
    name = "gnc"
    section = "combustible"
    default = decimal.Decimal(1)
    required = True


def global_parameters(param):
    global_preferences = global_preferences_registry.manager()
    return global_preferences[param]


def get_cotizacion_dolar():
    return global_parameters("cotizacion_dolar")


def get_modulo_tributario():
    return global_parameters("modulo_tributario")


def get_valor_litro(tipo_combustible):
    tipo = tipo_combustible.lower().replace(" ", "_")
    return global_parameters(f"combustible__{tipo}")
