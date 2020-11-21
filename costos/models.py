import decimal
from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel


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


class ParametroGlobal(TimeStampedModel):
    cotizacion_dolar = models.DecimalField("cotización del dólar", max_digits=8, decimal_places=2)
    modulo_tributario = models.DecimalField("módulo tributario SCIT", max_digits=8, decimal_places=2)

    class Meta:
        ordering = ["-modified"]
        verbose_name = "parámetro global"
        verbose_name_plural = "parámetros globales"

    def __str__(self):
        return str(self.modified)


class Empresa(models.Model):
    nombre = models.CharField(max_length=100, blank=True)
    horas_semanales = models.PositiveSmallIntegerField(default=40)

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
        return round(sum([gasto.semanal for gasto in self.gastos.all()]), 2)

    @property
    def gastos_por_hora(self):
        """Gastos por hora de trabajo en la Oficina de la Empresa."""
        return round(self.gastos_semanales / self.horas_semanales, 2)

    @property
    def gastos_mensuales(self):
        """Gastos por mes de trabajo en la Oficina de la Empresa."""
        return round(sum([gasto.mensual for gasto in self.gastos.all()]), 2)

    @property
    def gastos_anuales(self):
        """Gastos por año de trabajo en la Oficina de la Empresa."""
        return round(sum([gasto.anual for gasto in self.gastos.all()]), 2)


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
        total_gastos_semanales = sum([gasto.semanal for gasto in self.gastos.all()])
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


class Combustible(TimeStampedModel):
    TIPO_COMBUSTIBLE = (
        ("n", "Nafta"),
        ("p", "Nafta Premium"),
        ("d", "Diesel"),
        ("l", "Diesel Premium"),
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
    valor = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor de reposición en pesos.")
    kilometraje_anual = models.PositiveIntegerField()
    tipo_combustible = models.ForeignKey(Combustible, on_delete=models.CASCADE)
    rendimiento = models.PositiveSmallIntegerField("rendimiento [km/l]", default=9)
    costo_patente = models.DecimalField(max_digits=8, decimal_places=2)
    costo_seguro = models.DecimalField(max_digits=8, decimal_places=2)
    costo_cochera = models.DecimalField(max_digits=8, decimal_places=2)
    costo_lubricante = models.DecimalField(max_digits=8, decimal_places=2)
    costo_lavado = models.DecimalField(max_digits=8, decimal_places=2)
    costo_neumatico = models.DecimalField(max_digits=8, decimal_places=2)
    costo_service = models.DecimalField(max_digits=8, decimal_places=2)
    costo_anual_reparaciones = models.DecimalField(max_digits=8, decimal_places=2)

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
    def combustible(self):
        return self.tipo_combustible.valor_litro / self.rendimiento

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
            + self.service,
            2,
        )


class Instrumento(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="instrumentos")
    nombre = models.CharField(max_length=30)
    valor_USD = models.DecimalField(max_digits=8, decimal_places=2, help_text="Cotización dólar según Banco Nación.")
    vida_util = models.PositiveIntegerField(
        "vida útil", default=200, help_text="Vida útil esperada en jornadas de medición/gabinete."
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
        GLOBAL = ParametroGlobal.objects.last() or False
        DOLAR = GLOBAL.cotizacion_dolar if GLOBAL else 0
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
    fecha = models.DateField()
    expediente = models.PositiveIntegerField(blank=True, null=True)
    comitente = models.CharField(max_length=50, blank=True)
    profesionales = models.ManyToManyField(Profesional, through="Actuantes")
    vehiculos = models.ManyToManyField(Vehiculo, through="Movilidad")
    instrumentos = models.ManyToManyField(Instrumento, through="Instrumental")
    aporte_copa = models.DecimalField(max_digits=10, decimal_places=2, default=2200)
    aporte_caja = models.DecimalField(max_digits=10, decimal_places=2, default=2890)
    partidas = models.PositiveSmallIntegerField(blank=True, default=1)
    lotes_finales = models.PositiveSmallIntegerField(blank=True, default=1)
    escrituras = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=1)
    visado_municipio = models.DecimalField(max_digits=8, decimal_places=2, blank=True, default=0)
    ccu = models.DecimalField("certificado catastral urgente", max_digits=8, decimal_places=2, blank=True, default=0)
    estudio_titulos = models.DecimalField("estudio de títulos", max_digits=8, decimal_places=2, blank=True, default=0)
    georreferenciacion = models.DecimalField(
        "georreferenciación", max_digits=8, decimal_places=2, blank=True, default=0
    )
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
        return f"{self.expediente}"

    trabajo = property(__str__)

    @property
    def sellado_fiscal(self):
        if self.partidas and self.lotes_finales:
            GLOBAL = ParametroGlobal.objects.last() or False
            MT = GLOBAL.modulo_tributario if GLOBAL else 0
            _91011 = 6 * 2 * MT
            _91066 = 300 * MT
            _95013 = 300 * MT
            _95068 = 300 * MT
            _95077 = 500 * MT
            return _91011 + _91066 + _95013 * self.partidas + _95068 * self.lotes_finales + _95077
        else:
            return 0

    @property
    def empresa(self):
        return self.actuantes.first().profesional.empresa

    @property
    def horas_total(self):
        return sum([p.horas for p in self.actuantes.all()])

    @property
    def gastos_de_empresa(self):
        return self.horas_total * self.empresa.gastos_por_hora

    @property
    def costo_de_profesionales(self):
        # return sum([f.horas * f.profesional.costo_por_hora for f in self.actuantes.all()])
        return 0

    @property
    def costo_movilidad(self):
        return sum([m.km * m.vehiculo.costo_km for m in self.movilidad_set.all()])

    @property
    def amortizacion_de_instrumentos(self):
        return sum([i.jornadas * i.instrumento.costo_jornada for i in self.instrumental_set.all()])

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
            + (self.costo_movilidad or 0)
            + (self.amortizacion_de_instrumentos or 0)
        )


class Actuantes(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE, related_name="actuantes")
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE, related_name="actuantes")
    horas = models.PositiveSmallIntegerField(
        default=10, help_text="Horas de medición, gabinete, gestiones y trámites."
    )

    class Meta:
        ordering = ["-horas", "profesional"]

    def __str__(self):
        return f"{self.trabajo} - {self.profesional} [{self.horas} hs]"


class Movilidad(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    km = models.PositiveSmallIntegerField(default=70, help_text="Kilomtraje estimado.")

    class Meta:
        ordering = ["-km", "vehiculo"]

    def __str__(self):
        return f"{self.trabajo} - {self.vehiculo} [{self.km} km]"


class Instrumental(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE)
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    jornadas = models.PositiveSmallIntegerField(default=1, help_text="Jornadas de utilización.")

    class Meta:
        ordering = ["-jornadas", "instrumento"]

    def __str__(self):
        return f"{self.trabajo} - {self.instrumento} [{self.jornadas} día/s]"
