from django.contrib.auth import mixins  # LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
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
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


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
            self.object = form.save()
            if formset.is_valid():
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


class EmpresaCreateView(ChildrenContextMixin, mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Empresa
    form_class = forms.EmpresaForm
    # ChildrenContextMixin params
    children = "gastos"
    fs = forms.GastosEmpresaInlineFormSet

    def form_valid(self, form):
        """Assign Empresa to the User who has created it."""
        instance = form.save()
        self.request.user.empresa = instance
        self.request.user.save()
        return super().form_valid(form)


class EmpresaUpdateView(EmpresaFilterMixin, ChildrenContextMixin, mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Empresa
    form_class = forms.EmpresaForm
    # ChildrenContextMixin params
    children = "gastos"
    fs = forms.GastosEmpresaInlineFormSet


class ProfesionalListView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.ListView):
    model = models.Profesional


class ProfesionalDetailView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Profesional
    form_class = forms.ProfesionalForm


class ProfesionalCreateView(EmpresaInitialMixin, mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Profesional
    form_class = forms.ProfesionalForm


class ProfesionalUpdateView(EmpresaFilterMixin, ChildrenContextMixin, mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Profesional
    form_class = forms.ProfesionalForm
    # ChildrenContextMixin params
    children = "gastos"
    fs = forms.GastosPersonalesInlineFormSet


class InstrumentoListView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.ListView):
    model = models.Instrumento


class InstrumentoDetailView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Instrumento
    form_class = forms.InstrumentoForm


class InstrumentoCreateView(EmpresaInitialMixin, mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Instrumento
    form_class = forms.InstrumentoForm


class InstrumentoUpdateView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Instrumento
    form_class = forms.InstrumentoForm


class InstrumentoDeleteView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Instrumento
    success_url = reverse_lazy("instrumento_list")


class VehiculoListView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.ListView):
    model = models.Vehiculo


class VehiculoDetailView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Vehiculo
    form_class = forms.VehiculoForm


class VehiculoCreateView(EmpresaInitialMixin, mixins.LoginRequiredMixin, generic.CreateView):
    model = models.Vehiculo
    form_class = forms.VehiculoForm


class VehiculoUpdateView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.UpdateView):
    model = models.Vehiculo
    form_class = forms.VehiculoForm


class VehiculoDeleteView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Vehiculo
    success_url = reverse_lazy("vehiculo_list")


class TrabajoListView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.ListView):
    model = models.Trabajo


class TrabajoDetailView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.DetailView):
    model = models.Trabajo
    form_class = forms.TrabajoForm


class TrabajoCreateView(
    CurrentUserMixin, EmpresaFilterMixin, TrabajoChildrenContextMixin, mixins.LoginRequiredMixin, generic.CreateView
):
    model = models.Trabajo
    form_class = forms.TrabajoForm


class TrabajoUpdateView(
    EmpresaFilterMixin, TrabajoChildrenContextMixin, mixins.LoginRequiredMixin, generic.UpdateView
):
    model = models.Trabajo
    form_class = forms.TrabajoForm


class TrabajoDeleteView(EmpresaFilterMixin, mixins.LoginRequiredMixin, generic.DeleteView):
    model = models.Trabajo
    success_url = reverse_lazy("trabajo_list")


@login_required
def user_preferences(request, section=None):
    form_class = forms.user_preferences_form(request.user, section)
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            for k, v in form.cleaned_data.items():
                request.user.preferences[k] = v
            request.user.save()
            return HttpResponseRedirect(reverse_lazy('trabajo_list'))
    else:
        form = form_class()

    return render(request, "costos/profesional_preferences.html", {"form": form})
