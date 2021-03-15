import csv

from copasfn.settings import DEFAULT_FROM_EMAIL
from django.contrib import messages
from django.contrib.auth import mixins  # LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import BadHeaderError, send_mail
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic  # ListView

from . import forms, models


class CounterMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["count"] = self.get_queryset().count()
        return context


class Home(generic.TemplateView):
    template_name = "index.html"


class CurrentUserMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class SuccessDeleteMessageMixin:
    def delete(self, request, *args, **kwargs):
        delete_message = self.success_message if hasattr(self, "success_message") else "Objeto eliminado con éxito"
        messages.success(self.request, delete_message)
        return super().delete(request, *args, **kwargs)


class EmpresaFilterMixin:
    def get_queryset(self):
        """
        Returns only objects related to the User's Empresa.
        """
        if self.request.user.empresa:
            if self.model == models.Empresa:
                qs = self.model.objects.filter(id=self.request.user.empresa.pk)
            elif self.model == models.Trabajo:
                # Special case for models.Trabajo
                socios = models.Profesional.objects.filter(empresa=self.request.user.empresa)
                qs = self.model.objects.filter(profesionales__in=socios).distinct()
            else:
                qs = self.model.objects.filter(empresa=self.request.user.empresa)
        elif self.model == models.Profesional:
            # In case the User has no Empresa yet
            qs = self.model.objects.filter(id=self.request.user.pk)
        else:
            qs = self.model.objects.none()
        return qs


class EmpresaInitialMixin:
    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        initial = super().get_initial()
        initial["empresa"] = self.request.user.empresa
        return initial


class ChildrenContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context[self.children] = self.fs(self.request.POST, instance=self.object)
        else:
            context[self.children] = self.fs(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context[self.children]
        with transaction.atomic():
            if formset.is_valid():
                # Save parent only if each formset is valid
                self.object = form.save()
                # Set instance and save formset
                formset.instance = self.object
                formset.save()
            else:
                return render(self.request, context["view"].get_template_names(), context)
        return super().form_valid(form)


class TrabajoChildrenContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["actuantes"] = forms.ActuantesInlineFormSet(self.request.POST, instance=self.object)
            context["movilidad"] = forms.MovilidadInlineFormSet(self.request.POST, instance=self.object)
            context["instrumental"] = forms.InstrumentalInlineFormSet(self.request.POST, instance=self.object)
        else:
            context["actuantes"] = forms.ActuantesInlineFormSet(instance=self.object)
            context["movilidad"] = forms.MovilidadInlineFormSet(instance=self.object)
            context["instrumental"] = forms.InstrumentalInlineFormSet(instance=self.object)
        # Set choices
        profesionales_qs = models.Profesional.objects.filter(empresa=self.request.user.empresa)
        vehiculos_qs = models.Vehiculo.objects.filter(empresa=self.request.user.empresa)
        instrumentos_qs = models.Instrumento.objects.filter(empresa=self.request.user.empresa)
        for form in context["actuantes"]:
            form.fields["profesional"].queryset = profesionales_qs
        for form in context["movilidad"]:
            form.fields["vehiculo"].queryset = vehiculos_qs
        for form in context["instrumental"]:
            form.fields["instrumento"].queryset = instrumentos_qs
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset_actuantes = context["actuantes"]
        formset_movilidad = context["movilidad"]
        formset_instrumental = context["instrumental"]
        with transaction.atomic():
            if (
                form.is_valid()
                and formset_actuantes.is_valid()
                and formset_movilidad.is_valid()
                and formset_instrumental.is_valid()
            ):
                # Save parent only if each formset is valid
                self.object = form.save()
                # Set instance and save formset
                formset_actuantes.instance = self.object
                formset_actuantes.save()
                formset_movilidad.instance = self.object
                formset_movilidad.save()
                formset_instrumental.instance = self.object
                formset_instrumental.save()
            else:
                return render(self.request, context["view"].get_template_names(), context)
        return super().form_valid(form)


class EmpresaDetailView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Empresa
    form_class = forms.EmpresaForm


class EmpresaCreateView(SuccessMessageMixin, ChildrenContextMixin, mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Empresa
    form_class = forms.EmpresaForm
    # ChildrenContextMixin params
    children = "gastos"
    fs = forms.GastosEmpresaInlineFormSet
    success_message = "¡Empresa <strong>%(nombre)s</strong> creada con éxito! Ud. ya puede comenzar a utilizar el sistema en todo su potencial."

    def form_valid(self, form):
        """Assign Empresa to the User who has created it, only if User do not have one yet."""
        if not self.request.user.empresa:
            instance = form.save()
            self.request.user.empresa = instance
            self.request.user.save()
            return super().form_valid(form)
        else:
            empresa = self.request.user.empresa
            message = f"""No tiene permitido crear una nueva Empresa porque
                Ud. ya pertenece a la Empresa <strong>{empresa}</strong>.<br>
                Si desea modificar la Empresa actual, presione en
                <a href="{empresa.get_update_url()}" class="alert-link">Editar</a>.<br>
                Si, en cambio, desea unirse a la empresa de otro Profesional,
                <a href="{reverse_lazy("contact")}" class="alert-link">contáctenos</a>."""
            messages.error(self.request, message % form.cleaned_data)
            return redirect(empresa)


class EmpresaUpdateView(
    EmpresaFilterMixin, SuccessMessageMixin, ChildrenContextMixin, mixins.LoginRequiredMixin, generic.UpdateView
):
    model = models.Empresa
    form_class = forms.EmpresaForm
    # ChildrenContextMixin params
    children = "gastos"
    fs = forms.GastosEmpresaInlineFormSet
    success_message = "Empresa <strong>%(nombre)s</strong> modificada con éxito."


class ProfesionalListView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.ListView):
    model = models.Profesional


class ProfesionalDetailView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Profesional
    form_class = forms.ProfesionalForm


class ProfesionalCreateView(SuccessMessageMixin, EmpresaInitialMixin, mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Profesional
    form_class = forms.ProfesionalForm
    success_message = "¡Profesional <strong>%(first_name)s %(last_name)s</strong> creado/a con éxito!"


class ProfesionalUpdateView(
    SuccessMessageMixin, EmpresaFilterMixin, ChildrenContextMixin, mixins.LoginRequiredMixin, generic.UpdateView
):
    model = models.Profesional
    form_class = forms.ProfesionalForm
    # ChildrenContextMixin params
    children = "gastos"
    fs = forms.GastosPersonalesInlineFormSet
    success_message = "Profesional <strong>%(first_name)s %(last_name)s</strong> modificado/a con éxito."


class InstrumentoListView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.ListView):
    model = models.Instrumento


class InstrumentoDetailView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Instrumento
    form_class = forms.InstrumentoForm


class InstrumentoCreateView(SuccessMessageMixin, EmpresaInitialMixin, mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Instrumento
    form_class = forms.InstrumentoForm
    success_message = "Instrumento <strong>%(nombre)s</strong> creado con éxito."


class InstrumentoUpdateView(SuccessMessageMixin, EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Instrumento
    form_class = forms.InstrumentoForm
    success_message = "Instrumento <strong>%(nombre)s</strong> modificado con éxito."


class InstrumentoDeleteView(
    SuccessDeleteMessageMixin, EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.DeleteView
):
    model = models.Instrumento
    success_url = reverse_lazy("instrumento_list")
    success_message = "Instrumento eliminado con éxito."


class VehiculoListView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.ListView):
    model = models.Vehiculo


class VehiculoDetailView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Vehiculo
    form_class = forms.VehiculoForm


class VehiculoCreateView(SuccessMessageMixin, EmpresaInitialMixin, mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Vehiculo
    form_class = forms.VehiculoForm
    success_message = "Vehículo <strong>%(nombre)s</strong> creado con éxito."


class VehiculoUpdateView(SuccessMessageMixin, EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Vehiculo
    form_class = forms.VehiculoForm
    success_message = "Vehículo <strong>%(nombre)s</strong> modificado con éxito."


class VehiculoDeleteView(SuccessDeleteMessageMixin, EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Vehiculo
    success_url = reverse_lazy("vehiculo_list")
    success_message = "Vehículo eliminado con éxito."


class TrabajoListView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.ListView):
    model = models.Trabajo


class TrabajoDetailView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Trabajo
    form_class = forms.TrabajoForm


class TrabajoCreateView(
    SuccessMessageMixin,
    CurrentUserMixin,
    EmpresaFilterMixin,
    TrabajoChildrenContextMixin,
    mixins.LoginRequiredMixin,
    generic.CreateView,
):
    model = models.Trabajo
    form_class = forms.TrabajoForm
    success_message = "Trabajo creado con éxito."


class TrabajoUpdateView(
    SuccessMessageMixin, EmpresaFilterMixin, TrabajoChildrenContextMixin, mixins.LoginRequiredMixin, generic.UpdateView
):
    model = models.Trabajo
    form_class = forms.TrabajoForm
    success_message = "Trabajo modificado con éxito."


class TrabajoDeleteView(SuccessDeleteMessageMixin, EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Trabajo
    success_url = reverse_lazy("trabajo_list")
    success_message = "Trabajo eliminado con éxito."


@login_required
def trabajo_csv(request, pk):
    # Get the object
    trabajo = models.Trabajo.objects.get(pk=pk)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{trabajo}.csv"'

    writer = csv.writer(response)
    writer.writerow(
        [
            "Fecha",
            "Expediente",
            "Comitente",
            "Horas",
            "Gastos de Empresa",
            "Costo de actuantes",
            "Costo de movilidad",
            "Costo de instrumental",
            "Aportes",
            "Demás gastos específicos",
            "Costo total",
        ]
    )
    writer.writerow(
        [
            trabajo.fecha,
            trabajo.expediente,
            trabajo.comitente,
            trabajo.horas_total,
            trabajo.gastos_de_empresa,
            trabajo.costo_actuantes,
            trabajo.costo_movilidad,
            trabajo.costo_instrumental,
            trabajo.aportes,
            trabajo.gastos_especificos,
            trabajo.costo_total,
        ]
    )

    return response


@login_required
def user_preferences(request, section=None):
    form_class = forms.user_preferences_form(request.user, section)
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            for k, v in form.cleaned_data.items():
                request.user.preferences[k] = v
            request.user.save()
            de_seccion = f"de {section}" if section else ""
            messages.success(request, f"Preferencias {de_seccion} guardadas con éxito.")
            return redirect("trabajo_list")
    else:
        form = form_class()

    return render(request, "costos/profesional_preferences.html", {"form": form})


@login_required
def contact_view(request, asunto="", mensaje=""):
    if request.method == "GET":
        form = forms.ContactForm(initial={"asunto": asunto or None, "mensaje": mensaje or None})
    else:
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["asunto"]
            message = f"{request.user} <{request.user.email}> escribió:\n\n{form.cleaned_data['mensaje']}"
            try:
                send_mail(
                    subject,
                    message,
                    DEFAULT_FROM_EMAIL,
                    [f"{request.user} <{request.user.email}>", DEFAULT_FROM_EMAIL],
                )
                messages.success(
                    request,
                    """<strong>¡Su mensaje fue enviado!</strong>
                    Nuestro Soporte Técnico le responderá a la brevedad.
                    Gracias por escribirnos.""",
                )
            except BadHeaderError:
                messages.error(request, "Encabezado no válido. No se pudo enviar.")
            return redirect("contact")
    return render(request, "costos/contacto.html", {"form": form})
