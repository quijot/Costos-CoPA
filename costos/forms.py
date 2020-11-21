from crispy_forms.bootstrap import FormActions, Tab, TabHolder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Div, Fieldset, Layout, Row, Submit
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
                    Fieldset("Gastos", Formset("gastos")),
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
                    Fieldset("Gastos", Formset("gastos")),
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
                            Div("costo_service", css_class="col-lg-6"),
                            Div("costo_anual_reparaciones", css_class="col-lg-6"),
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
