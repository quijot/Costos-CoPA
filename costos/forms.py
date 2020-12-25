from crispy_forms.bootstrap import FormActions, Tab, TabHolder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Button, Div, Field, Fieldset, Layout, Row, Submit
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy

from . import models
from .formset_layout import Formset


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = models.Empresa
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    "Empresa",
                    Fieldset(
                        "Características",
                        Row(
                            Div("nombre", css_class="col-lg-8"),
                            Div("horas_semanales", css_class="col-lg-4"),
                        ),
                    ),
                    Fieldset(
                        "Gastos",
                        HTML(
                            """<div class="alert alert-primary alert-dismissible fade show" role="alert">
                            Cargar todos los gastos asociados únicamente a la Empresa / Oficina.
                            NO se cargan aquí los gastos asociados a los Profesionales que la conforman
                            (salvo que así lo decidan sus miembros).
                            Ejemplos:
                            Alquiler, Impuestos y Servicios propios de la locación, Limpieza, Publicidad,
                            Hosting, Licencias de Software, Sueldos, etc.
                            <button type="button" class="close" data-dismiss="alert" aria-label="Cerrar">
                                <span aria-hidden="true">&times;</span>
                            </button>
                            </div>"""
                        ),
                        Formset("gastos"),
                    ),
                    FormActions(
                        Button(
                            "cancel",
                            "Cancelar",
                            css_class="btn-dark",
                            onclick=f"window.location.href = '{reverse_lazy('instrumento_list')}';",
                        ),
                        Submit("save", "Guardar"),
                        css_class="float-right",
                    ),
                ),
            )
        )


GastosEmpresaInlineFormSet = forms.inlineformset_factory(
    models.Empresa,
    models.GastoEmpresa,
    fields=("tipo", "monto", "periodo", "descripcion"),
    extra=10,
)


class ProfesionalForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = models.Profesional
        fields = (
            "last_name",
            "first_name",
            "email",
            "empresa",
            "matricula",
            "cuit",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    "Profesional",
                    Fieldset(
                        "Datos personales",
                        Row(
                            Div("empresa", css_class="d-none"),
                        ),
                        Row(
                            Div("last_name", css_class="col-lg-6"),
                            Div("first_name", css_class="col-lg-6"),
                        ),
                        Row(
                            Div("matricula", css_class="col-lg-2"),
                            Div("email", css_class="col-lg-6"),
                            Div("cuit", css_class="col-lg-4"),
                        ),
                    ),
                    Fieldset(
                        "Gastos",
                        HTML(
                            """<div class="alert alert-info alert-dismissible fade show" role="alert">
                            Cargar todos los gastos asociados únicamente a este Profesional.
                            NO se cargan aquí los gastos asociados a la Empresa / Oficina.
                            Ejemplos:
                            Matrícula, Monotributo, Jubilación, Obra Social, posiblemente algún Seguro,
                            Capacitación, Celular, etc. <strong>Los gastos asociados a un Profesional
                            formaran parte del costo por hora de su <em>mano de obra</em></strong>.
                            <button type="button" class="close" data-dismiss="alert" aria-label="Cerrar">
                                <span aria-hidden="true">&times;</span>
                            </button>
                            </div>"""
                        ),
                        Formset("gastos"),
                    ),
                    FormActions(
                        Button(
                            "cancel",
                            "Cancelar",
                            css_class="btn-dark",
                            onclick=f"window.location.href = '{reverse_lazy('profesional_list')}';",
                        ),
                        Submit("save", "Guardar"),
                        css_class="float-right",
                    ),
                ),
            )
        )


GastosPersonalesInlineFormSet = forms.inlineformset_factory(
    models.Profesional,
    models.GastoPersonal,
    fields=("tipo", "monto", "periodo", "descripcion"),
    extra=10,
)


class InstrumentoForm(forms.ModelForm):
    class Meta:
        model = models.Instrumento
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    "Instrumento",
                    Fieldset(
                        "Características",
                        Row(
                            Div("empresa", css_class="d-none"),
                        ),
                        Row(
                            Div("nombre", css_class="col-lg-12"),
                        ),
                        Row(
                            Div("valor_USD", css_class="col-lg-6"),
                            Div("vida_util", css_class="col-lg-6"),
                        ),
                        Row(
                            Div(
                                Div(
                                    HTML(
                                        """¿Cómo calcular la <em>Vida útil</em> del instrumento?
                                        <small id="hint_id_vida_util" class="form-text text-muted">
                                        Estimar los siguientes valores:<br>
                                        <strong>A</strong>: cantidad de años en que quisiera recuperar
                                        el valor invertido y <strong>reponer el instrumento</strong>,<br>
                                        <strong>T</strong>: promedio de trabajos realizados por año,<br>
                                        <strong>J</strong>: jornadas de este instrumento que se suelen
                                        dedicar a cada trabajo. Ejemplo: para una Estación Total puede
                                        ser 1 jornada por trabajo, pero para una PC pueden ser 4.<br>
                                        <strong>Resultado</strong>: haciendo <strong>A &times; T &times; J</strong>
                                        se obtiene un número aproximado de jornadas de vida útil.<br>
                                        <strong>Ejemplo</strong>: Estación Total, A=5 (5 años de vida útil),
                                        T=40 (40 trabajos por año), J=1 (1 jornada por trabajo). 5 &times; 40
                                        &times; 1 = 200 jornadas de vida útil.</small>
                                        <button type="button" class="close" data-dismiss="alert" aria-label="Cerrar">
                                            <span aria-hidden="true">&times;</span>
                                        </button>"""
                                    ),
                                    css_class="alert alert-warning alert-dismissible fade show",
                                ),
                                css_class="col",
                            )
                        ),
                    ),
                    FormActions(
                        Button(
                            "cancel",
                            "Cancelar",
                            css_class="btn-dark",
                            onclick=f"window.location.href = '{reverse_lazy('instrumento_list')}';",
                        ),
                        Submit("save", "Guardar"),
                        css_class="float-right",
                    ),
                ),
            )
        )


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = models.Vehiculo
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    "Vehiculo",
                    Fieldset(
                        "Características",
                        Row(
                            Div("empresa", css_class="d-none"),
                        ),
                        Row(
                            Div("nombre", css_class="col-lg-8"),
                            Div("valor", css_class="col-lg-4"),
                        ),
                        Row(
                            Div("kilometraje_anual", css_class="col-lg-4"),
                            Div("tipo_combustible", css_class="col-lg-4"),
                            Div("rendimiento", css_class="col-lg-4"),
                        ),
                    ),
                    Fieldset(
                        "Mantenimiento",
                        Row(
                            Div("costo_patente", css_class="col-lg-4"),
                            Div("costo_seguro", css_class="col-lg-4"),
                            Div("costo_cochera", css_class="col-lg-4"),
                        ),
                        Row(
                            Div("costo_lubricante", css_class="col-lg-4"),
                            Div("costo_lavado", css_class="col-lg-4"),
                            Div("costo_neumatico", css_class="col-lg-4"),
                        ),
                        Row(
                            Div("costo_service", css_class="col-lg-4"),
                            Div("costo_anual_reparaciones", css_class="col-lg-4"),
                            Div("costo_rto", css_class="col-lg-4"),
                        ),
                    ),
                    FormActions(
                        Button(
                            "cancel",
                            "Cancelar",
                            css_class="btn-dark",
                            onclick=f"window.location.href = '{reverse_lazy('vehiculo_list')}';",
                        ),
                        Submit("save", "Guardar"),
                        css_class="float-right",
                    ),
                ),
            )
        )


ActuantesInlineFormSet = forms.inlineformset_factory(
    models.Trabajo,
    models.Actuantes,
    fields=("profesional", "horas"),
    extra=3,
    min_num=1,
    validate_min=True,
)


MovilidadInlineFormSet = forms.inlineformset_factory(
    models.Trabajo,
    models.Movilidad,
    fields=("vehiculo", "km"),
    extra=2,
)


InstrumentalInlineFormSet = forms.inlineformset_factory(
    models.Trabajo,
    models.Instrumental,
    fields=("instrumento", "jornadas"),
    extra=5,
)


class TrabajoForm(forms.ModelForm):
    class Meta:
        model = models.Trabajo
        fields = [
            "fecha",
            "expediente",
            "comitente",
            "aporte_copa",
            "aporte_caja",
            "partidas",
            "lotes_finales",
            "escrituras",
            "visados",
            "ccu",
            "estudio_titulos",
            "georreferenciacion",
            "citaciones",
            "viaticos",
            "ayudante",
            "dibujante",
            "impresiones",
            "mojones",
            "gestor",
            "seguros_especiales",
            "alquiler_instrumentos",
            "otros_gastos",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML(
                """<div class="alert alert-danger alert-dismissible fade show" role="alert">
            Antes de guardar, recuerde asignar al menos un profesional actuante en la
            pestaña <strong>Profesionales.</strong>
            <button type="button" class="close" data-dismiss="alert" aria-label="Cerrar">
                <span aria-hidden="true">&times;</span>
            </button>
            </div>"""
            ),
            TabHolder(
                Tab(
                    "Trabajo",
                    Fieldset(
                        "",
                        Row(
                            Div(Field("fecha", css_class="date", id="datepicker"), css_class="col-lg-3"),
                            Div("expediente", css_class="col-lg-3"),
                            Div("comitente", css_class="col-lg-6"),
                        ),
                    ),
                    Fieldset(
                        "Gastos típicos de Mensura",
                        Row(
                            Div("aporte_copa", css_class="col-lg-6"),
                            Div("aporte_caja", css_class="col-lg-6"),
                        ),
                        Row(
                            Div("partidas", css_class="col-lg-3"),
                            Div("lotes_finales", css_class="col-lg-3"),
                            Div("escrituras", css_class="col-lg-3"),
                            Div("visados", css_class="col-lg-3"),
                        ),
                    ),
                    Fieldset(
                        "Gastos en jornadas de medición",
                        Row(
                            Div("ayudante", css_class="col-lg-4"),
                            Div("viaticos", css_class="col-lg-4"),
                            Div("mojones", css_class="col-lg-4"),
                        ),
                        Row(
                            Div("alquiler_instrumentos", css_class="col-lg-6"),
                            Div("seguros_especiales", css_class="col-lg-6"),
                        ),
                    ),
                    Fieldset(
                        "Gastos por presentaciones",
                        Row(
                            Div("dibujante", css_class="col-lg-4"),
                            Div("impresiones", css_class="col-lg-4"),
                            Div("gestor", css_class="col-lg-4"),
                        ),
                    ),
                ),
                Tab("Profesionales", Formset("actuantes")),
                Tab("Vehículos", Formset("movilidad")),
                Tab("Instrumentos", Formset("instrumental")),
                Tab(
                    "Gastos especiales",
                    Fieldset(
                        "Gastos por trámites extra",
                        Row(
                            Div("ccu", css_class="col-lg-3"),
                            Div("estudio_titulos", css_class="col-lg-3"),
                            Div("georreferenciacion", css_class="col-lg-3"),
                            Div("citaciones", css_class="col-lg-3"),
                        ),
                    ),
                    Fieldset(
                        "Otros",
                        Row(
                            Div("otros_gastos", css_class="col-lg-12"),
                        ),
                    ),
                ),
            ),
            FormActions(
                Button(
                    "cancel",
                    "Cancelar",
                    css_class="btn-dark",
                    onclick=f"window.location.href = '{reverse_lazy('trabajo_list')}';",
                ),
                Submit("save", "Guardar"),
                css_class="float-right",
            ),
        )
