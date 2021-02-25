import decimal
from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .preferences import get_cotizacion_dolar, get_modulo_tributario, get_valor_litro


class Periodo(Enum):
    DIA = 1
    SEMANA = 7
    QUINCENA = 15
    MES = 30
    BIMESTRE = 60
    TRIMESTRE = 90
    CUATRIMESTRE = 120
    SEMESTRE = 180
    AÑO = 360


class Empresa(models.Model):
    nombre = models.CharField(max_length=100, blank=True)
    horas_semanales = models.PositiveSmallIntegerField(default=40, help_text="Horas de trabajo por semana.")

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("empresa_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("empresa_update", kwargs={"pk": self.pk})

    # def has_change_permission(self, request, obj=None):
    #     if obj is not None and obj.pk != request.user.empresa.pk:
    #         return False
    #     return True

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
    def gastos_semanales(self):
        """Gastos por semana de trabajo en la Oficina de la Empresa."""
        return round(decimal.Decimal(sum([gasto.semanal for gasto in self.gastos.all()])), 2)

    @property
    def gastos_por_hora(self):
        """Gastos por hora de trabajo en la Oficina de la Empresa."""
        return round(self.gastos_semanales / self.horas_semanales, 2)

    @property
    def gastos_mensuales(self):
        """Gastos por mes de trabajo en la Oficina de la Empresa."""
        return round(decimal.Decimal(sum([gasto.mensual for gasto in self.gastos.all()])), 2)

    @property
    def gastos_anuales(self):
        """Gastos por año de trabajo en la Oficina de la Empresa."""
        return round(decimal.Decimal(sum([gasto.anual for gasto in self.gastos.all()])), 2)


class Profesional(AbstractUser):
    empresa = models.ForeignKey(Empresa, blank=True, null=True, on_delete=models.PROTECT, related_name="profesionales")
    matricula = models.CharField("matrícula", max_length=7, unique=True, blank=True, null=True)
    cuit = models.CharField("CUIT", max_length=14, blank=True)

    class Meta:
        ordering = ["matricula"]
        verbose_name_plural = "profesionales"

    def __str__(self):
        if self.matricula and self.apellido and self.nombre:
            return f"{self.matricula} - {self.apellido.upper()} {self.nombre}"
        else:
            return self.username

    def get_absolute_url(self):
        return reverse("profesional_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("profesional_update", kwargs={"pk": self.pk})

    @property
    def apellido(self):
        return self.last_name

    @property
    def nombre(self):
        return self.first_name

    @property
    def costo_por_hora(self):
        """Costo de 1 hora de trabajo del Profesional."""
        total_gastos_semanales = decimal.Decimal(sum([gasto.semanal for gasto in self.gastos.all()]))
        return round(total_gastos_semanales / self.empresa.horas_semanales, 2) if self.empresa else 0

    @property
    def gastos_semanales(self):
        """Costo por semana de trabajo del Profesional."""
        return round(sum([gasto.semanal for gasto in self.gastos.all()]), 2)

    @property
    def gastos_por_hora(self):
        """Costo por hora de trabajo del Profesional."""
        return round(self.gastos_semanales / self.horas_semanales, 2)

    @property
    def gastos_mensuales(self):
        """Costo por mes de trabajo del Profesional."""
        return round(sum([gasto.mensual for gasto in self.gastos.all()]), 2)

    @property
    def gastos_anuales(self):
        """Costo por año de trabajo del Profesional."""
        return round(sum([gasto.anual for gasto in self.gastos.all()]), 2)


class Vehiculo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="vehiculos")
    nombre = models.CharField(max_length=30)
    valor = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor de reposición actualizado en pesos.")
    kilometraje_anual = models.PositiveIntegerField(default=20000, help_text="KM estimados para un año.")
    TIPO_COMBUSTIBLE = (
        ("n", "Nafta"),
        ("p", "Nafta Premium"),
        ("d", "Diesel"),
        ("l", "Diesel Premium"),
        ("g", "GNC"),
    )
    tipo_combustible = models.CharField(max_length=1, choices=TIPO_COMBUSTIBLE, default="n")
    rendimiento = models.PositiveSmallIntegerField(
        "rendimiento [km/l]", default=9, help_text="Rendimiento promedio en km por litro."
    )
    costo_patente = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Costo de cada cuota de la patente."
    )
    costo_seguro = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Costo mensual del seguro."
    )
    costo_cochera = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Costo mensual de cochera / garage."
    )
    costo_lubricante = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Costo del lubricante (calcula cada 6 meses)."
    )
    costo_lavado = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Gastos mensuales en lavado."
    )
    costo_neumatico = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Costo de 1 neumático (calcula cada 40.000 km)."
    )
    costo_service = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Costo de Service general (calcula cada 10.000 km)."
    )
    costo_anual_reparaciones = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Estimado de reparaciones por año."
    )
    costo_rto = models.DecimalField(
        "RTO", max_digits=8, decimal_places=2, default=0, help_text="Costo de Revisión Técnica Obligatoria."
    )

    class Meta:
        ordering = ["nombre", "valor"]
        verbose_name = "vehículo"
        verbose_name_plural = "vehículos"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("vehiculo_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("vehiculo_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("vehiculo_delete", kwargs={"pk": self.pk})

    @property
    def combustible_valor(self):
        return get_valor_litro(self.get_tipo_combustible_display())

    @property
    def combustible(self):
        return self.combustible_valor / self.rendimiento

    @property
    def valor_residual(self):
        """Valor residual a 5 años."""
        return self.valor / 2 if self.valor else 0

    @property
    def amortizacion_valor(self):
        if self.valor:
            return (self.valor - self.valor_residual) / (5 * self.kilometraje_anual)
        else:
            return 0

    @property
    def kilometraje_mensual(self):
        return round(self.kilometraje_anual / decimal.Decimal(12), 2) if self.kilometraje_anual else 1

    @property
    def amortizacion_seguro(self):
        return round(self.costo_seguro / self.kilometraje_mensual, 2) if self.costo_seguro else 0

    @property
    def amortizacion_patente(self):
        return round(self.costo_patente / 2 / self.kilometraje_mensual, 2) if self.costo_patente else 0

    @property
    def amortizacion_cochera(self):
        return round(self.costo_cochera / self.kilometraje_mensual, 2) if self.costo_cochera else 0

    @property
    def amortizacion_lavado(self):
        return round(self.costo_lavado / self.kilometraje_mensual, 2) if self.costo_lavado else 0

    @property
    def amortizacion_neumaticos(self):
        return round(self.costo_neumatico * 4 / 40000, 2) if self.costo_neumatico else 0

    @property
    def reparaciones(self):
        return round(self.costo_anual_reparaciones / self.kilometraje_anual, 2) if self.costo_anual_reparaciones else 0

    @property
    def repuestos(self):
        return round(self.valor * decimal.Decimal(0.02), 2) if self.valor else 0

    @property
    def repuestos_por_km(self):
        return round(self.repuestos / self.kilometraje_anual, 2) if self.valor else 0

    @property
    def service(self):
        return round(self.costo_service / 10000, 2) if self.costo_service else 0

    @property
    def lubricacion(self):
        return round(self.costo_lubricante * 2 / self.kilometraje_anual, 2) if self.costo_lubricante else 0

    @property
    def rto(self):
        return round(self.costo_rto / (2 * self.kilometraje_anual), 2) if self.costo_rto else 0

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
            + self.repuestos_por_km
            + self.amortizacion_neumaticos
            + self.service
            + self.rto,
            2,
        )


class Instrumento(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="instrumentos")
    nombre = models.CharField(max_length=30)
    valor_USD = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Valor de reposición en dólares. Cotización dólar oficial según Banco Nación.",
    )
    vida_util = models.PositiveIntegerField(
        "vida útil",
        default=200,
        help_text="Vida útil esperada en jornadas de trabajo y/o gabinete.",
    )

    class Meta:
        ordering = ["nombre", "valor_USD"]

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("instrumento_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("instrumento_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("instrumento_delete", kwargs={"pk": self.pk})

    @property
    def valor_ARS(self):
        DOLAR = get_cotizacion_dolar()
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
        (Periodo.DIA.value, "Diario"),
        (Periodo.SEMANA.value, "Semanal"),
        (Periodo.MES.value, "Mensual"),
        (Periodo.BIMESTRE.value, "Bimestral"),
        (Periodo.TRIMESTRE.value, "Trimestral"),
        (Periodo.CUATRIMESTRE.value, "Cuatrimestral"),
        (Periodo.SEMESTRE.value, "Semestral"),
        (Periodo.AÑO.value, "Anual"),
    )
    periodo = models.PositiveSmallIntegerField(choices=PERIODO, default=Periodo.MES.value)

    class Meta:
        ordering = ["tipo", "-monto"]
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
        return round(self.jornada * Periodo.SEMANA.value, 2)

    @property
    def mensual(self):
        return round(self.jornada * Periodo.MES.value, 2)

    @property
    def anual(self):
        return round(self.jornada * Periodo.AÑO.value, 2)


class GastoEmpresa(Gasto):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="gastos")

    class Meta:
        ordering = ["tipo", "-monto"]
        verbose_name = "gasto general"
        verbose_name_plural = "gastos generales"


class GastoPersonal(Gasto):
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name="gastos")

    class Meta:
        ordering = ["tipo", "-monto"]
        verbose_name = "gasto personal"
        verbose_name_plural = "gastos personales"


class Trabajo(models.Model):
    fecha = models.DateField(default=timezone.now, help_text="Fecha de cálculo de costos.")
    expediente = models.PositiveIntegerField(blank=True, null=True, help_text="Expediente CoPA relacionado.")
    comitente = models.CharField(max_length=50, blank=True)
    profesionales = models.ManyToManyField(Profesional, through="Actuantes")
    vehiculos = models.ManyToManyField(Vehiculo, through="Movilidad", blank=True)
    instrumentos = models.ManyToManyField(Instrumento, through="Instrumental", blank=True)
    aporte_copa = models.DecimalField(
        "aportes CoPA", max_digits=10, decimal_places=2, default=2200, help_text="Monto calculado según Sistema."
    )
    aporte_caja = models.DecimalField(
        "aportes Caja", max_digits=10, decimal_places=2, default=2890, help_text="Monto calculado según Sistema."
    )
    partidas = models.PositiveSmallIntegerField(
        "cantidad de partidas", default=1, help_text="Para cálculo de Sellados Fiscales e Informes Catastrales."
    )
    lotes_finales = models.PositiveSmallIntegerField(default=1, help_text="Para cálculo de Sellados Fiscales.")
    escrituras = models.DecimalField(
        "monto por escrituras", max_digits=8, decimal_places=2, default=0, help_text="Gasto por pedidos al RGP."
    )
    visados = models.DecimalField(
        "monto por visados", max_digits=8, decimal_places=2, default=0, help_text="Gastos en reparticiones públicas."
    )
    ccu = models.DecimalField(
        "Certificado Catastral Urgente",
        max_digits=8,
        decimal_places=2,
        default=0,
        help_text="Pago de sellados por CCU.",
    )
    estudio_titulos = models.DecimalField(
        "estudio de títulos",
        max_digits=8,
        decimal_places=2,
        default=0,
        help_text="Gastos extra por Estudio de Títulos.",
    )
    georreferenciacion = models.DecimalField(
        "georreferenciación",
        max_digits=8,
        decimal_places=2,
        default=0,
        help_text="Gastos extra por Georreferenciación.",
    )
    citaciones = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Pago de envío / estampillados por notificaciones."
    )
    viaticos = models.DecimalField(
        "viáticos", max_digits=8, decimal_places=2, default=0, help_text="Pago de alojamiento / comidas."
    )
    ayudante = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Pago de jornales a ayudante/s."
    )
    dibujante = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Pago a dibujante/s.")
    impresiones = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Pago por ploteos / impresiones de documentación."
    )
    mojones = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Gasto en hierros, estacas, pintura, cintas peligro."
    )
    gestor = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Pago a gestores, comisionistas, fletes."
    )
    seguros_especiales = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Pago de seguros ocasionales para este trabajo."
    )
    alquiler_instrumentos = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        help_text="Pago de alquileres ocasionales para este trabajo.",
    )
    otros_gastos = models.DecimalField(
        max_digits=8, decimal_places=2, default=0, help_text="Otros gastos sin categorizar."
    )

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.expediente}" if self.expediente else "S_N"

    trabajo = property(__str__)

    def get_absolute_url(self):
        return reverse("trabajo_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("trabajo_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("trabajo_delete", kwargs={"pk": self.pk})

    def get_csv_url(self):
        return reverse("trabajo_csv", kwargs={"pk": self.pk})

    @property
    def empresa(self):
        return self.profesionales.first().empresa if self.profesionales.last() else None

    @property
    def cantidad_de_profesionales(self):
        return self.profesionales.count()

    cantidad_de_profesionales.fget.short_description = "# profesionales"

    @property
    def cantidad_de_instrumentos(self):
        return self.instrumental.count()

    cantidad_de_instrumentos.fget.short_description = "# instrumentos"

    @property
    def cantidad_de_vehiculos(self):
        return self.movilidad.count()

    cantidad_de_vehiculos.fget.short_description = "# vehículos"

    @property
    def horas_total(self):
        return sum([p.horas for p in self.actuantes.all()])

    @property
    def aportes(self):
        return self.aporte_copa + self.aporte_caja

    @property
    def sellado_fiscal(self):
        if self.partidas and self.lotes_finales:
            MT = get_modulo_tributario()
            _91011 = 6 * 2 * MT
            _91066 = 300 * MT
            _95013 = 300 * MT
            _95068 = 300 * MT
            _95077 = 500 * MT
            return _91011 + _91066 + _95013 * self.partidas + _95068 * self.lotes_finales + _95077
        else:
            return 0

    @property
    def informe_catastral(self):
        MT = get_modulo_tributario()
        INFORME_CATASTRAL = 400 * MT
        return INFORME_CATASTRAL * self.partidas

    @property
    def gastos_de_empresa(self):
        if self.empresa:
            return self.horas_total * self.empresa.gastos_por_hora
        else:
            return 0

    @property
    def costo_actuantes(self):
        return round(decimal.Decimal(sum([f.horas * f.profesional.costo_por_hora for f in self.actuantes.all()])), 2)

    @property
    def costo_movilidad(self):
        return round(decimal.Decimal(sum([m.km * m.vehiculo.costo_km for m in self.movilidad.all()])), 2)

    @property
    def cantidad_de_km(self):
        return sum([m.km for m in self.movilidad.all()])

    @property
    def costo_instrumental(self):
        return round(
            decimal.Decimal(sum([i.jornadas * i.instrumento.costo_jornada for i in self.instrumental.all()])), 2
        )

    @property
    def cantidad_de_jornadas(self):
        return sum([i.jornadas for i in self.instrumental.all()])

    @property
    def gastos_especificos(self):
        return (
            self.escrituras
            + self.visados
            + self.ccu
            + self.estudio_titulos
            + self.georreferenciacion
            + self.citaciones
            + self.viaticos
            + self.ayudante
            + self.dibujante
            + self.impresiones
            + self.mojones
            + self.gestor
            + self.seguros_especiales
            + self.alquiler_instrumentos
            + self.otros_gastos
            + self.sellado_fiscal
            + self.informe_catastral
        )

    @property
    def costo_total(self):
        return (
            self.aportes
            + self.gastos_especificos
            + self.gastos_de_empresa
            + self.costo_actuantes
            + self.costo_movilidad
            + self.costo_instrumental
        )

    @property
    def proporcion_empresa(self):
        return round(self.gastos_de_empresa / self.costo_total * 100, 1)

    @property
    def proporcion_actuantes(self):
        return round(self.costo_actuantes / self.costo_total * 100, 1)

    @property
    def proporcion_movilidad(self):
        return round(self.costo_movilidad / self.costo_total * 100, 1)

    @property
    def proporcion_instrumental(self):
        return round(self.costo_instrumental / self.costo_total * 100, 1)

    @property
    def proporcion_aportes(self):
        return round(self.aportes / self.costo_total * 100, 1)

    @property
    def proporcion_especificos(self):
        return round(self.gastos_especificos / self.costo_total * 100, 1)


class Actuantes(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, related_name="actuantes")
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name="actuante")
    horas = models.PositiveSmallIntegerField(default=10, help_text="Medición, gabinete, gestiones y trámites.")

    class Meta:
        ordering = ["-horas", "profesional"]

    def __str__(self):
        return f"{self.trabajo} - {self.profesional} [{self.horas} hs]"


class Movilidad(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, related_name="movilidad")
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name="trabajos")
    km = models.PositiveSmallIntegerField(default=70, help_text="Kilometraje estimado.")

    class Meta:
        ordering = ["-km", "vehiculo"]

    def __str__(self):
        return f"{self.trabajo} - {self.vehiculo} [{self.km} km]"


class Instrumental(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, related_name="instrumental")
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE, related_name="trabajos")
    jornadas = models.PositiveSmallIntegerField(default=1, help_text="Jornadas de utilización.")

    class Meta:
        ordering = ["-jornadas", "instrumento"]

    def __str__(self):
        return f"{self.trabajo} - {self.instrumento} [{self.jornadas} día/s]"
