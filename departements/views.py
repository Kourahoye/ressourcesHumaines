from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView,DeleteView,UpdateView
from employees.models import Employee
from .models import Departements
from .forms import DepartementsForm
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from collections import defaultdict
from django.utils.timezone import now
from evaluations.models import DepartementRating
from django.db.models import Avg


class DepartementsCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    permission_required =["departements.add_departements"]
    login_url = reverse_lazy("login")

    model = Departements
    form_class = DepartementsForm
    template_name = 'departements/create.html'
    success_url = reverse_lazy('liste_departements')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context

    def form_valid(self, form):

        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    
    


class DepartementsListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required =["departements.view_departements"]

    login_url = reverse_lazy("login")
    model = Departements
    template_name = 'departements/list.html'
    context_object_name = 'departements'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context






class DepartementsDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = ["departements.view_departements"]
    login_url = reverse_lazy("login")
    model = Departements
    template_name = 'departements/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departement = self.get_object()
        context['permissions'] = list(self.request.user.get_all_permissions())
        context['employees'] = Employee.objects.filter(departement=departement)

        # --- Partie chart progression note par mois ---
        current_year = str(now().year)
        mois_dict = {
            1: 'Janvier', 2: 'Fevrier', 3: 'Mars', 4: 'Avril',
            5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Aout',
            9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Decembre'
        }

        # Récupérer toutes les notes pour ce département et année courante
        notes_qs = DepartementRating.objects.filter(
            departement=departement,
            year=current_year
        ).order_by('month')

        # Conversion mois texte -> numéro
        def mois_texte_to_num(mois):
            mapping = {v: k for k, v in mois_dict.items()}
            return mapping.get(mois, 0)

        # Créer un mapping mois_num -> note (moyenne par mois s'il y a plusieurs)
        # Ici, on prend la moyenne par mois
        from django.db.models import Avg
        notes_par_mois = (
            notes_qs.values('month')
            .annotate(moyenne=Avg('note'))
            .order_by('month')
        )
        # Dictionnaire mois_num -> moyenne
        mois_to_note = {mois_texte_to_num(entry['month']): entry['moyenne'] for entry in notes_par_mois}

        labels = [mois_dict[i] for i in range(1, 13)]
        data = [mois_to_note.get(i, 0) for i in range(1, 13)]

        context['chart_labels'] = labels
        context['chart_data'] = data

        notes_qs = DepartementRating.objects.filter(
            departement=departement
        ).values('year').annotate(moyenne=Avg('note')).order_by('year')

        years = [entry['year'] for entry in notes_qs]
        moyennes = [round(entry['moyenne'], 2) for entry in notes_qs]

        context['chart_labels_year'] = years
        context['chart_data_year'] = moyennes

        return context

    
    
class DepartementsDeleteView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    permission_required =["departements.delete_departements"]

    model = Departements
    template_name = 'departements/delete.html'
    success_url = reverse_lazy('liste_departements')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
    

class DepartementsUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required =["departements.update_departements"]

    model = Departements
    template_name = 'departements/update.html'
    form_class = DepartementsForm
    success_url = reverse_lazy('liste_departements')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

