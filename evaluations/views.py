from collections import defaultdict
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView,ListView,TemplateView
from django.db.models import OuterRef,Subquery,F

from employees.models import Employee
from .forms import DepartementRateForm, EmployeeRateForm
from .models import DepartementRating, EmployeeRating


mois_fr = {
        1: 'Janvier', 2: 'Fevrier', 3: 'Mars', 4: 'Avril',
        5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Aout',
        9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
    }

mois_courant = mois_fr[timezone.now().month]

# Create your views here.
class DepartementRatingCreateView(CreateView):
    model = DepartementRating
    form_class = DepartementRateForm
    template_name = "evaluations/departements/create.html"
    success_url = reverse_lazy("departements_notes")
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        # form.instance.month = timezone.now().month
        # form.instance.year = timezone.now().year
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
    
class DepartementRatingList(ListView):
    model = DepartementRating
    context_object_name = 'notes'
    template_name="evaluations/departements/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        context['current'] = DepartementRating.objects.all().filter(year=timezone.now().year)
        return context


class EmployeeRatingCreateView(CreateView):
    model = EmployeeRating
    form_class = EmployeeRateForm
    template_name = "evaluations/employees/create.html"
    success_url = reverse_lazy("employees_notes")
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        # form.instance.month = timezone.now().month
        # form.instance.year = timezone.now().year
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
        
    
class EmployeeRatingList(ListView):
    model = EmployeeRating
    context_object_name = 'notes'
    template_name="evaluations/employees/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        context['current'] = EmployeeRating.objects.all().filter(year=timezone.now().year)
        return context


from django.db.models import Avg
from django.utils.timezone import now

def classement_departement_annee_en_cours():
    current_year = str(now().year)
    return (
        DepartementRating.objects
        .filter(year=current_year)
        .order_by('-note')  # Classement de l'année en cours
    )

def classement_departement_annees_prec():
    current_year = str(now().year)
    return (
        DepartementRating.objects
        .exclude(year=current_year)
        .values('departement', 'year')  # Grouper par departement + année
        .annotate(moyenne_note=Avg('note'))  # Calculer moyenne
        .order_by('-moyenne_note')
    )



class ClassementEmployee(TemplateView):
    template_name="evaluations/employees/classement.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year = str(now().year)
        subquery = (
            EmployeeRating.objects
            .filter(employee=OuterRef("employee"),year=OuterRef('year'))
            .exclude(year=current_year)
            .annotate(moyenne=Avg("note"))
            # .values("employee__user__username")
            .values('moyenne')[:1]
                )
        notes = EmployeeRating.objects.all().annotate(moyenne_note=Subquery(subquery)).order_by('-moyenne_note').exclude(year=current_year)
        seen = set()
        grouped_by_year = defaultdict(list)
        for obj in notes:
            key = (obj.employee_id, obj.year)
            if key not in seen:
                seen.add(key)
                grouped_by_year[obj.year].append(obj)

        context['permissions'] = list(self.request.user.get_all_permissions())
        context['current']=EmployeeRating.objects.filter(year=current_year).order_by('-note')
        context['grouped_by_year'] = list(grouped_by_year.items())
        return context

class ClassementDepartement(TemplateView):
    
    template_name="evaluations/departements/classement.html"
    
   
    def get_context_data(self, **kwargs):
        current_year = str(now().year)
        moyenne_sousrequete = (
        DepartementRating.objects.filter(departement=OuterRef('departement'), year=OuterRef('year'))
        .values('departement', 'year')
        .annotate(moyenne=Avg('note'))
        .values('moyenne')[:1]
        )
        queryset = (
            DepartementRating.objects
            # .distinct('departement','year')
            .exclude(year=current_year)
            .annotate(moyenne_note=Subquery(moyenne_sousrequete))
            .order_by('-moyenne_note')
            # .select_related('departement')  # Pour accéder à nom, etc.
        )
        seen = set()
        grouped_by_year = defaultdict(list)

        for obj in queryset:
            key = (obj.departement_id, obj.year)
            if key not in seen:
                seen.add(key)
                grouped_by_year[obj.year].append(obj)
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        context['grouped_by_year']= list(grouped_by_year.items())
        context['current'] = DepartementRating.objects.all().filter(year=current_year,month=mois_courant).order_by('-note','departement_id')
        return context


