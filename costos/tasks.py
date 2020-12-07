import decimal

import requests

from costos import models


def cotizacion_dolar():
    """Scrap cotización del Dólar desde el sitio del BNA"""
    from django.db import connection
    connection.close()
    bna = requests.get("https://bna.com.ar/")
    cotizacion = decimal.Decimal(bna.text.partition("U.S.A")[2].split("<td>")[2].partition("<")[0].replace(",", "."))
    if cotizacion:
        params = models.ParametroGlobal.objects.last()
        params.cotizacion_dolar = cotizacion
        params.save()
