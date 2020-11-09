import decimal

from django.contrib.auth.models import AbstractUser
from django.db import models

DOLAR = decimal.Decimal(84.25)


class Empresa(models.Model):
    nombre = models.CharField(max_length=100, blank=True)
    # cuit = models.CharField("CUIT", max_length=14, blank=True)
    horas_semanales = models.PositiveSmallIntegerField(default=40)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    @property
    def cantidad_de_profesionales(self):
        return self.profesionales.count()

    cantidad_de_profesionales.fget.short_description = "# profesionales"

    @property
    def cantidad_de_vehiculos(self):
        return self.vehiculos.count()

    cantidad_de_vehiculos.fget.short_description = "# vehículos"

    @property
    def cantidad_de_instrumentos(self):
        return self.instrumentos.count()

    cantidad_de_instrumentos.fget.short_description = "# instrumentos"

    @property
    def gastos_por_hora(self):
        """Gastos por cada 1 hora de trabajo en la Oficina de la Empresa."""
        # promedio_semanas_al_mes = 365 / 7 / 12
        # promedio_horas_mensuales = self.horas_semanales * promedio_semanas_al_mes
        # total_gastos_mensuales = sum([gasto.mensual for gasto in self.gastos.all()])
        total_gastos_semanales = sum([gasto.semanal for gasto in self.gastos.all()])
        # return round(total_gastos_mensuales / decimal.Decimal(promedio_horas_mensuales), 2)
        return round(total_gastos_semanales / self.horas_semanales, 2)


class Profesional(AbstractUser):
    empresa = models.ForeignKey(Empresa, null=True, on_delete=models.PROTECT, related_name="profesionales")
    matricula = models.CharField("matrícula", max_length=7, unique=True)
    cuit = models.CharField("CUIT", max_length=14, blank=True)

    class Meta:
        ordering = ["matricula"]
        verbose_name_plural = "profesionales"

    def __str__(self):
        return f"{self.matricula} - {self.apellido.upper()} {self.nombre}"

    @property
    def apellido(self):
        return self.last_name

    @property
    def nombre(self):
        return self.first_name

    @property
    def costo_por_hora(self):
        """Costo de 1 hora de trabajo del Profesional."""
        # promedio_semanas_al_mes = 365 / 7 / 12
        # promedio_horas_mensuales = self.horas_semanales * promedio_semanas_al_mes
        # total_gastos_mensuales = sum([gasto.mensual for gasto in self.gastos.all()])
        # return round(total_gastos_mensuales / decimal.Decimal(promedio_horas_mensuales), 2)
        total_gastos_semanales = sum([gasto.semanal for gasto in self.gastos.all()])
        return round(total_gastos_semanales / self.empresa.horas_semanales, 2) if self.empresa else 0


class Combustible(models.Model):
    TIPO_COMBUSTIBLE = (
        ("p", "Nafta Premium"),
        ("n", "Nafta"),
        ("l", "Diesel Premium"),
        ("d", "Diesel"),
        ("g", "GNC"),
    )
    combustible = models.CharField(max_length=1, choices=TIPO_COMBUSTIBLE, default="n")
    valor_litro = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ["combustible"]

    def __str__(self):
        return self.get_combustible_display()


class Vehiculo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="vehiculos")
    nombre = models.CharField(max_length=30)
    valor_a_nuevo = models.DecimalField(max_digits=10, decimal_places=2)
    kilometraje_anual = models.PositiveIntegerField()
    tipo_combustible = models.ForeignKey(Combustible, on_delete=models.CASCADE)
    rendimiento = models.PositiveSmallIntegerField("rendimiento [km/l]", default=9)
    costo_mensual_patente = models.DecimalField(max_digits=8, decimal_places=2)
    costo_mensual_seguro = models.DecimalField(max_digits=8, decimal_places=2)
    costo_mensual_cochera = models.DecimalField(max_digits=8, decimal_places=2)
    costo_lubricante = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    costo_lavado = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    costo_neumatico = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    costo_service = models.DecimalField(max_digits=8, decimal_places=2)
    costo_anual_reparaciones = models.DecimalField(max_digits=8, decimal_places=2, blank=True)

    class Meta:
        ordering = ["nombre", "valor_a_nuevo"]
        verbose_name = "vehículo"
        verbose_name_plural = "vehículos"

    def __str__(self):
        return self.nombre

    @property
    def combustible(self):
        return self.tipo_combustible.valor_litro / self.rendimiento

    @property
    def valor_residual(self):
        """Valor residual a 5 años."""
        return self.valor_a_nuevo / 2 if self.valor_a_nuevo else 0

    @property
    def amortizacion_valor(self):
        if self.valor_a_nuevo:
            return (self.valor_a_nuevo - self.valor_residual) / (5 * self.kilometraje_anual)
        else:
            return 0

    @property
    def kilometraje_mensual(self):
        return self.kilometraje_anual / decimal.Decimal(12) if self.kilometraje_anual else 1

    @property
    def amortizacion_seguro(self):
        return self.costo_mensual_seguro / self.kilometraje_mensual if self.costo_mensual_seguro else 0

    @property
    def amortizacion_patente(self):
        return self.costo_mensual_patente / self.kilometraje_mensual if self.costo_mensual_patente else 0

    @property
    def amortizacion_cochera(self):
        return self.costo_mensual_cochera / self.kilometraje_mensual if self.costo_mensual_cochera else 0

    @property
    def amortizacion_lavado(self):
        return self.costo_lavado / self.kilometraje_mensual if self.costo_lavado else 0

    @property
    def amortizacion_neumaticos(self):
        return self.costo_neumatico * 4 / 40000 if self.costo_neumatico else 0

    @property
    def reparaciones(self):
        return self.costo_anual_reparaciones / self.kilometraje_anual if self.costo_anual_reparaciones else 0

    @property
    def respuestos(self):
        return self.valor_a_nuevo * decimal.Decimal(0.02) / self.kilometraje_anual if self.valor_a_nuevo else 0

    @property
    def service(self):
        return self.costo_service / 10000 if self.costo_service else 0

    @property
    def lubricacion(self):
        return self.costo_lubricante * 2 / self.kilometraje_anual if self.costo_lubricante else 0

    @property
    def costo_km(self):
        return round(
            self.amortizacion_valor
            + self.amortizacion_seguro
            + self.amortizacion_patente
            + self.amortizacion_cochera
            + self.combustible
            + self.lubricacion
            + self.amortizacion_lavado
            + self.reparaciones
            + self.respuestos
            + self.amortizacion_neumaticos
            + self.service,
            2,
        )


class Instrumento(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="instrumentos")
    nombre = models.CharField(max_length=30)
    valor_USD = models.DecimalField(max_digits=8, decimal_places=2)
    vida_util = models.PositiveIntegerField(
        "vida útil", default=5, help_text="Vida útil esperada en jornadas de medición."
    )

    class Meta:
        ordering = ["nombre", "valor_USD"]

    def __str__(self):
        return self.nombre

    @property
    def valor_ARS(self):
        return round(self.valor_USD * DOLAR, 2) if self.pk else 0

    valor_ARS.fget.short_description = "valor ARS"

    @property
    def costo_jornada(self):
        return round(self.valor_ARS / self.vida_util, 2)


class TipoGasto(models.Model):
    detalle = models.CharField(max_length=50)

    class Meta:
        ordering = ["detalle"]
        verbose_name = "tipo de gasto"
        verbose_name_plural = "tipos de gastos"

    def __str__(self):
        return self.detalle


class Gasto(models.Model):
    tipo = models.ForeignKey(TipoGasto, on_delete=models.CASCADE)
    descripcion = models.CharField("descripción", max_length=100, blank=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    PERIODO = (
        (1, "Diario"),
        (7, "Semanal"),
        (30, "Mensual"),
        (60, "Bimestral"),
        (90, "Trimestral"),
        (120, "Cuatrimestral"),
        (180, "Semestral"),
        (365, "Anual"),
    )
    periodo = models.PositiveSmallIntegerField(choices=PERIODO, default="30")

    class Meta:
        ordering = ["tipo"]
        abstract = True
        verbose_name = "gasto"
        verbose_name_plural = "gastos"

    def __str__(self):
        return self.tipo.detalle

    @property
    def jornada(self):
        return self.monto / self.periodo

    @property
    def semanal(self):
        return self.jornada * 7

    @property
    def mensual(self):
        return self.jornada * 30


class GastoEmpresa(Gasto):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="gastos")

    class Meta:
        verbose_name = "gasto general"
        verbose_name_plural = "gastos generales"


class GastoPersonal(Gasto):
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name="gastos")

    class Meta:
        verbose_name = "gasto personal"
        verbose_name_plural = "gastos personales"


class Trabajo(models.Model):
    fecha = models.DateField()
    expediente = models.PositiveIntegerField(blank=True, null=True)
    comitente = models.CharField(max_length=50)
    profesionales = models.ManyToManyField(Profesional, related_name="trabajos")
    vehiculos = models.ManyToManyField(Vehiculo, related_name="trabajos", blank=True)
    instrumentos = models.ManyToManyField(Instrumento, related_name="trabajos", blank=True)
    aporte_copa = models.DecimalField(max_digits=10, decimal_places=2, default=2200)
    aporte_caja = models.DecimalField(max_digits=10, decimal_places=2, default=2890)
    partidas = models.PositiveSmallIntegerField(blank=True, default=1)
    lotes_finales = models.PositiveSmallIntegerField(blank=True, default=1)
    distancia_km = models.PositiveIntegerField(blank=True, default=70)
    horas = models.PositiveSmallIntegerField(default=10, help_text="Horas de medición, gabinete, gestiones y trámites.")
    jornadas_de_medicion = models.PositiveSmallIntegerField(
        "jornadas de medición", default=1, help_text="Jornadas de utilización de instrumentos."
    )
    escrituras = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=1)
    visado_municipio = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=0)
    ccu = models.DecimalField("certificado catastral urgente", max_digits=8, decimal_places=2, blank=True, default=0)
    estudio_titulos = models.DecimalField("estudio de títulos", max_digits=8, decimal_places=2, blank=True, default=0)
    georreferenciacion = models.DecimalField("georreferenciación", max_digits=8, decimal_places=2, blank=True, default=0)
    citaciones = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=0)
    ayudante = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=0)
    dibujante = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=0)
    impresiones = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=0)
    mojones = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=0)
    gestor = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=0)
    seguros_especiales = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=0)
    alquiler_instrumentos = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=0)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.expediente} - {self.comitente}"

    trabajo = property(__str__)

    @property
    def sellado_fiscal(self):
        if self.partidas and self.lotes_finales:
            _91011 = 9
            _91066 = 225
            _95013 = 225
            _95068 = 225
            _95077 = 375
            return _91011 + _91066 + _95013 * self.partidas + _95068 * self.lotes_finales + _95077
        else:
            return 0

    @property
    def empresa(self):
        return self.profesionales.first().empresa

    @property
    def gastos_de_empresa(self):
        return self.horas * self.empresa.gastos_por_hora

    @property
    def costo_de_profesionales(self):
        return self.horas * sum([p.costo_por_hora for p in self.profesionales.all()])

    @property
    def movilidad(self):
        return self.distancia_km * sum([v.costo_km for v in self.vehiculos.all()])

    @property
    def amortizacion_de_instrumentos(self):
        return self.jornadas_de_medicion * sum([i.costo_jornada for i in self.instrumentos.all()])

    @property
    def costo_total(self):
        return (
            (self.aporte_copa or 0)
            + (self.aporte_caja or 0)
            + (self.escrituras or 0)
            + (self.visado_municipio or 0)
            + (self.ccu or 0)
            + (self.estudio_titulos or 0)
            + (self.georreferenciacion or 0)
            + (self.citaciones or 0)
            + (self.ayudante or 0)
            + (self.dibujante or 0)
            + (self.impresiones or 0)
            + (self.mojones or 0)
            + (self.gestor or 0)
            + (self.seguros_especiales or 0)
            + (self.alquiler_instrumentos or 0)
            + (self.gastos_de_empresa or 0)
            + (self.costo_de_profesionales or 0)
            + (self.movilidad or 0)
            + (self.amortizacion_de_instrumentos or 0)
        )
