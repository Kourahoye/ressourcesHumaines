from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,DeleteView,DetailView,UpdateView
from evaluations.models import EmployeeRating
from presences.models import Presence
from .models import Employee
from .forms import EmployeeForm
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.db.models import Q,Avg
from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Count
import calendar

    

class EmployeeCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required =['employees.add_employee']
    login_url = reverse_lazy("login")
    
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/create.html'
    success_url = reverse_lazy('employee_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context


    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class EmployeeDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = ['employees.view_employee']
    login_url = reverse_lazy("login")
    model = Employee
    template_name = 'employees/profil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.get_object()
        context['permissions'] = list(self.request.user.get_all_permissions())
        current_year = now().year
        mois_dict = {
            1: 'Janvier', 2: 'Fevrier', 3: 'Mars', 4: 'Avril',
            5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Aout',
            9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Decembre'
        }

        # Récupérer toutes les notes pour ce département et année courante
        notes_qs = EmployeeRating.objects.filter(
            employee=employee,
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

        notes_qs = EmployeeRating.objects.filter(
            employee=employee
        ).values('year').annotate(moyenne=Avg('note')).order_by('year')

        years = [entry['year'] for entry in notes_qs]
        moyennes = [round(entry['moyenne'], 2) for entry in notes_qs]

        context['chart_labels_year'] = years
        context['chart_data_year'] = moyennes
        #absences
       

    

        # Requête ORM
        absences_raw = (
            Presence.objects
            .filter(employee_id=self.get_object(), is_absent=True)
            .annotate(mois=ExtractMonth('date'), annee=ExtractYear('date'))
            .values('annee', 'mois')
            .annotate(total_absences=Count('id'))
            .order_by('annee', 'mois')
        )
        absences_formatees = [
            {
                "periode": f"{mois_dict[item['mois']]}",
                "absences": item["total_absences"]
            }
            for item in absences_raw
        ]
        # print(absences_raw)
        context['absence_label'] = [item["periode"] for item in absences_formatees]
        context['absence_data'] = [item["absences"] for item in absences_formatees]

        return context

    
class EmployeeDeleteView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    permission_required =['employees.delete_employee']
    login_url = reverse_lazy("login")
    
    model = Employee
    template_name = "employees/delete.html"
    success_url = reverse_lazy('employee_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context


# class EmployeeDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    # permission_required = ['employees.view_employee']
    # login_url = reverse_lazy("login")
    # model = Employee
    # template_name = 'employees/profil.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['permissions'] = list(self.request.user.get_all_permissions())

    #     employee = self.get_object()
    #     current_year = now().year

    #     mois_dict = {
    #         1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril',
    #         5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Août',
    #         9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
    #     }

  

    #     presences_qs = Presence.objects.filter(
    #         employee=employee,
    #         date__year=current_year
    #     )

    #     presences_par_mois = (
    #         presences_qs
    #         .annotate(month=ExtractMonth('date'))
    #         .values('month')
    #         .annotate(count=Count('id'))
    #         .order_by('month')
    #     )

    #     mois_to_count = {entry['month']: entry['count'] for entry in presences_par_mois}

    #     labels = [mois_dict[i] for i in range(1, 13)]
    #     data = [mois_to_count.get(i, 0) for i in range(1, 13)]

    #     context['chart_labels'] = labels
    #     context['chart_data'] = data

    #     return context
    
    
    
class EmployeeUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required = ["employees.change_employee"]
    login_url = reverse_lazy("login")
    
    model = Employee
    form_class = EmployeeForm
    template_name='employees/update.html'
    success_url = reverse_lazy('employee_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    
    


  


class EmployeeListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required =['employees.list_employee']
    login_url = reverse_lazy("login")
    
    model = Employee
    template_name = 'employees/list.html'
    context_object_name = 'employees'
    # paginate_by = 10  
    
    def get_queryset(self):
        from django.db.models import Q
        if self.request.user.is_superuser:
            employees = Employee.objects.all()
        else:
            employees = Employee.objects.filter(
                Q(created_by=self.request.user) | Q(user=self.request.user)
            )
        return employees
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
    
    
