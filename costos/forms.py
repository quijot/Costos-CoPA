from crispy_forms.bootstrap import Alert, AppendedText, FormActions, PrependedText, Tab, TabHolder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Div, Field, Fieldset, Layout, Row, Submit
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy
from dynamic_preferences.users.forms import user_preference_form_builder

from . import models
from .formset_layout import Formset


class ContactForm(forms.Form):
    asunto = forms.CharField(required=True)
    mensaje = forms.CharField(widget=forms.Textarea, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("asunto"),
            Field("mensaje"),
            FormActions(
                Button(
                    "cancel",
                    "Cancelar",
                    css_class="btn-dark",
                    onclick=f"window.location.href = '{reverse_lazy('index')}';",
                ),
                Submit("save", "Enviar"),
                style="text-align: right;",
            ),
        )


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
                            Div(AppendedText("horas_semanales", "hs/sem"), css_class="col-lg-4"),
                        ),
                    ),
                    Fieldset(
                        "Gastos",
                        Alert(
                            content="""Cargar todos los gastos asociados únicamente a la Empresa / Oficina.
                            NO se cargan aquí los gastos asociados a los Profesionales que la conforman
                            (salvo que así lo decidan sus miembros).
                            Ejemplos:
                            Alquiler, Impuestos y Servicios propios de la locación, Limpieza, Publicidad,
                            Hosting, Licencias de Software, Sueldos, etc.""",
                            css_class="alert-primary alert-dismissible fade show",
                        ),
                        Button(
                            "add-gasto",
                            "&plus; Agregar Gasto",
                            css_class="btn-sm btn-danger",
                            title="Agregar otro Gasto",
                            onclick="add_form('gastos')",
                        ),
                        Formset("gastos"),
                    ),
                ),
            ),
            FormActions(
                Button(
                    "cancel",
                    "Cancelar",
                    css_class="btn-dark",
                    onclick=f"window.location.href = '{reverse_lazy('index')}';",
                ),
                Submit("save", "Guardar"),
                style="text-align: right;",
            ),
        )


GastosEmpresaInlineFormSet = forms.inlineformset_factory(
    models.Empresa,
    models.GastoEmpresa,
    fields=("tipo", "monto", "periodo", "descripcion"),
    extra=1,
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
                        Alert(
                            content="""Cargar todos los gastos asociados únicamente a este Profesional.
                            NO se cargan aquí los gastos asociados a la Empresa / Oficina.
                            Ejemplos:
                            Matrícula, Monotributo, Jubilación, Obra Social, posiblemente algún Seguro,
                            Capacitación, Celular, etc. <strong>Los gastos asociados a un Profesional
                            formaran parte del costo por hora de su <em>mano de obra</em></strong>.""",
                            css_class="alert-info alert-dismissible fade show",
                        ),
                        Button(
                            "add-gasto",
                            "&plus; Agregar Gasto",
                            css_class="btn-sm btn-danger",
                            title="Agregar otro Gasto",
                            onclick="add_form('gastos')",
                        ),
                        Formset("gastos"),
                    ),
                ),
            ),
            FormActions(
                Button(
                    "cancel",
                    "Cancelar",
                    css_class="btn-dark",
                    onclick=f"window.location.href = '{reverse_lazy('profesional_list')}';",
                ),
                Submit("save", "Guardar"),
                style="text-align: right;",
            ),
        )


GastosPersonalesInlineFormSet = forms.inlineformset_factory(
    models.Profesional,
    models.GastoPersonal,
    fields=("tipo", "monto", "periodo", "descripcion"),
    extra=1,
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
                            Div(PrependedText("valor_USD", "U$D"), css_class="col-lg-6"),
                            Div(AppendedText("vida_util", "jornadas"), css_class="col-lg-6"),
                        ),
                        Row(
                            Div(
                                Alert(
                                    content="""¿Cómo calcular la <em>Vida útil</em> del instrumento?
                                    <small id="hint_id_vida_util" class="form-text text-muted">
                                    Estimar los siguientes valores:<br>
                                    <strong>A</strong>: cantidad de años en que quisiera recuperar
                                    el valor invertido y <strong>reponer el instrumento</strong>,<br>
                                    <strong>T</strong>: promedio de trabajos realizados por año,<br>
                                    <strong>J</strong>: jornadas de este instrumento que se suelen
                                    dedicar a cada trabajo. Ejemplo: para una Estación Total puede
                                    ser 1 jornada por trabajo, pero para una PC pueden ser 4.<br>
                                    <strong>Resultado</strong>:
                                    haciendo <strong>A &times; T &times; J</strong> se obtiene un
                                    número aproximado de jornadas de vida útil.<br>
                                    <strong>Ejemplo</strong>: Estación Total, A=5 (5 años de vida útil),
                                    T=40 (40 trabajos por año), J=1 (1 jornada por trabajo). 5 &times;
                                    40 &times; 1 = 200 jornadas de vida útil.</small>""",
                                    css_class="alert-warning alert-dismissible fade show",
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
                            Div(PrependedText("valor", "AR$"), css_class="col-lg-4"),
                        ),
                        Row(
                            Div(AppendedText("kilometraje_anual", "km/año"), css_class="col-lg-4"),
                            Div("tipo_combustible", css_class="col-lg-4"),
                            Div(AppendedText("rendimiento", "km/lt"), css_class="col-lg-4"),
                        ),
                    ),
                    Fieldset(
                        "Mantenimiento",
                        Row(
                            Div(PrependedText("costo_patente", "$"), css_class="col-lg-4"),
                            Div(PrependedText("costo_seguro", "$"), css_class="col-lg-4"),
                            Div(PrependedText("costo_cochera", "$"), css_class="col-lg-4"),
                        ),
                        Row(
                            Div(PrependedText("costo_lubricante", "$"), css_class="col-lg-4"),
                            Div(PrependedText("costo_lavado", "$"), css_class="col-lg-4"),
                            Div(PrependedText("costo_neumatico", "$"), css_class="col-lg-4"),
                        ),
                        Row(
                            Div(PrependedText("costo_service", "$"), css_class="col-lg-4"),
                            Div(PrependedText("costo_anual_reparaciones", "$"), css_class="col-lg-4"),
                            Div(PrependedText("costo_rto", "$"), css_class="col-lg-4"),
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


class ActuantesForm(forms.ModelForm):
    profesional = forms.ModelChoiceField(models.Profesional.objects.none())

    class Meta:
        model = models.Actuantes
        fields = "__all__"


ActuantesInlineFormSet = forms.inlineformset_factory(
    models.Trabajo,
    models.Actuantes,
    form=ActuantesForm,
    fields=("profesional", "horas"),
    extra=1,
    min_num=1,
    validate_min=True,
)


class MovilidadForm(forms.ModelForm):
    vehiculo = forms.ModelChoiceField(models.Vehiculo.objects.none())

    class Meta:
        model = models.Movilidad
        fields = "__all__"


MovilidadInlineFormSet = forms.inlineformset_factory(
    models.Trabajo,
    models.Movilidad,
    form=MovilidadForm,
    fields=("vehiculo", "km"),
    extra=1,
)


class InstrumentalForm(forms.ModelForm):
    instrumento = forms.ModelChoiceField(models.Instrumento.objects.none())

    class Meta:
        model = models.Instrumental
        fields = "__all__"


InstrumentalInlineFormSet = forms.inlineformset_factory(
    models.Trabajo,
    models.Instrumental,
    form=InstrumentalForm,
    fields=("instrumento", "jornadas"),
    extra=1,
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
        user = kwargs.pop("user", None)
        # now kwargs doesn't contain 'user', so we can safely pass it to the base class method
        super().__init__(*args, **kwargs)
        # set all user preferences as initial values
        if user:
            user_pref = [
                "visados",
                "ayudante",
                "viaticos",
                "mojones",
                "alquiler_instrumentos",
                "seguros_especiales",
                "dibujante",
                "impresiones",
                "gestor",
                "otros_gastos",
            ]
            for pref in user_pref:
                self.initial[pref] = user.preferences[f"trabajo__{pref}"]
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Alert(
                content="""Antes de guardar, recuerde asignar al menos un profesional
                actuante en la pestaña <strong>Profesionales.</strong>""",
                css_class="alert-danger alert-dismissible fade show",
            ),
            TabHolder(
                Tab(
                    "Trabajo",
                    Fieldset(
                        "",
                        Row(
                            Div(Field("fecha", css_class="date", id="datepicker"), css_class="col-lg-3"),
                            Div(PrependedText("expediente", "N&ordm;"), css_class="col-lg-3"),
                            Div("comitente", css_class="col-lg-6"),
                        ),
                    ),
                    Fieldset(
                        "Gastos típicos de Mensura",
                        Row(
                            Div(PrependedText("aporte_copa", "$"), css_class="col-lg-6"),
                            Div(PrependedText("aporte_caja", "$"), css_class="col-lg-6"),
                        ),
                        Row(
                            Div("partidas", css_class="col-lg-3"),
                            Div("lotes_finales", css_class="col-lg-3"),
                            Div(PrependedText("escrituras", "$"), css_class="col-lg-3"),
                            Div(PrependedText("visados", "$"), css_class="col-lg-3"),
                        ),
                    ),
                    Fieldset(
                        "Gastos en jornadas de medición",
                        Row(
                            Div(PrependedText("ayudante", "$"), css_class="col-lg-4"),
                            Div(PrependedText("viaticos", "$"), css_class="col-lg-4"),
                            Div(PrependedText("mojones", "$"), css_class="col-lg-4"),
                        ),
                        Row(
                            Div(PrependedText("alquiler_instrumentos", "$"), css_class="col-lg-6"),
                            Div(PrependedText("seguros_especiales", "$"), css_class="col-lg-6"),
                        ),
                    ),
                    Fieldset(
                        "Gastos por presentaciones",
                        Row(
                            Div(PrependedText("dibujante", "$"), css_class="col-lg-4"),
                            Div(PrependedText("impresiones", "$"), css_class="col-lg-4"),
                            Div(PrependedText("gestor", "$"), css_class="col-lg-4"),
                        ),
                    ),
                    Fieldset(
                        "Otros",
                        Row(
                            Div(PrependedText("otros_gastos", "$"), css_class="col-lg-12"),
                        ),
                    ),
                ),
                Tab(
                    "Profesionales",
                    Button(
                        "add-profesional",
                        "&plus; Agregar Profesional",
                        css_class="btn-sm btn-info",
                        title="Agregar otro/a Profesional",
                        onclick="add_form('actuantes')",
                    ),
                    Formset("actuantes"),
                ),
                Tab(
                    "Vehículos",
                    Button(
                        "add-vehiculo",
                        "&plus; Agregar Vehículo",
                        css_class="btn-sm btn-success",
                        title="Agregar otro Vehículo",
                        onclick="add_form('movilidad')",
                    ),
                    Formset("movilidad"),
                ),
                Tab(
                    "Instrumentos",
                    Button(
                        "add-instrumento",
                        "&plus; Agregar Instrumento",
                        css_class="btn-sm btn-warning",
                        title="Agregar otro Instrumento",
                        onclick="add_form('instrumental')",
                    ),
                    Formset("instrumental"),
                ),
                Tab(
                    "Gastos especiales",
                    Fieldset(
                        "Gastos por trámites extra",
                        Row(
                            Div(PrependedText("ccu", "$"), css_class="col-lg-3"),
                            Div(PrependedText("estudio_titulos", "$"), css_class="col-lg-3"),
                            Div(PrependedText("georreferenciacion", "$"), css_class="col-lg-3"),
                            Div(PrependedText("citaciones", "$"), css_class="col-lg-3"),
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
                style="text-align: right;",
            ),
        )


def user_preferences_form(instance, section=None):
    form = user_preference_form_builder(instance=instance, section=section)
    form.helper = FormHelper()
    form.helper.layout = Layout(
        TabHolder(
            Tab(
                "Trabajos",
                Alert(
                    content="""Cargue aquí los valores más habituales para sus trabajos, de esta manera,
                    se cargarán <strong>por defecto</strong> cada vez que agregue un nuevo Trabajo.""",
                    css_class="alert-dark alert-dismissible fade show",
                ),
                Fieldset(
                    "Gastos típicos de Mensura",
                    Row(
                        Div(PrependedText("trabajo__visados", "$"), css_class="col-lg-3"),
                    ),
                ),
                Fieldset(
                    "Gastos en jornadas de medición",
                    Row(
                        Div(PrependedText("trabajo__ayudante", "$"), css_class="col-lg-4"),
                        Div(PrependedText("trabajo__viaticos", "$"), css_class="col-lg-4"),
                        Div(PrependedText("trabajo__mojones", "$"), css_class="col-lg-4"),
                    ),
                    Row(
                        Div(PrependedText("trabajo__alquiler_instrumentos", "$"), css_class="col-lg-6"),
                        Div(PrependedText("trabajo__seguros_especiales", "$"), css_class="col-lg-6"),
                    ),
                ),
                Fieldset(
                    "Gastos por presentaciones",
                    Row(
                        Div(PrependedText("trabajo__dibujante", "$"), css_class="col-lg-4"),
                        Div(PrependedText("trabajo__impresiones", "$"), css_class="col-lg-4"),
                        Div(PrependedText("trabajo__gestor", "$"), css_class="col-lg-4"),
                    ),
                ),
                Fieldset(
                    "Otros",
                    Row(
                        Div(PrependedText("trabajo__otros_gastos", "$"), css_class="col-lg-12"),
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
            style="text-align: right;",
        ),
    )

    return form
