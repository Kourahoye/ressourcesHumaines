from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from comptabilite.models import Salary
from conges.models import CongesRequest, User
from departements.models import Departements
from employees.models import Employee
from presences.models import Presence 
from django.db.models import Count
from django.db.models import Q
from django.db.models import Sum
from django.utils.timezone import now
from django.urls import reverse_lazy
from presences.models import Presence
from django.db.models.functions import ExtractMonth
from django.contrib.sessions.models import Session
from django.utils import timezone
# Create your views here.

class Dasbord(LoginRequiredMixin,TemplateView):
    template_name = "mainpage/dashbord.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        me = self.request.user
        users = User.objects.all()
        user_close = users.filter(is_active=False)
        departement_cpt = Departements.objects.all()
        employee_cpt = Employee.objects.all()
        employee_added = employee_cpt.filter(created_by = me)
        departement_added = departement_cpt.filter(created_by = me)
        free = User.objects.filter(is_active=True, profil_employee__conges__status=True).distinct().count()
        genres = User.objects.aggregate(
            hommes=Count('id', filter=Q(gender='masculin')),
            femmes=Count('id', filter=Q(gender='feminin'))
        )
        employees_absent = Presence.objects.filter(is_absent=True).filter(date=now().date()).distinct()
        try:
            if me.profil_employee:
                absence = Presence.objects.filter(employee=me.profil_employee, is_absent=True,date__month=now().month,date__year=now().year).count()
        except Exception as e:
            absence = 0
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        uid_list = []
        for session in sessions:
            data = session.get_decoded()
            uid = data.get('_auth_user_id')
            if uid:
                uid_list.append(uid)
        logged_in = User.objects.filter(id__in=uid_list, is_active=True).count()
        # print(f"Logged in users: {logged_in}")

        qs = Presence.objects.filter(
            is_absent=True,
            date__year=now().year
        ).annotate(
            month=ExtractMonth('date')
        ).values('month').order_by('month').annotate(total=Count('id'))
        qs2 = CongesRequest.objects.filter(
            created_at__year=now().year
        ).aggregate(
            accepted=Count('id', filter=Q(status='accepted')),
            refused=Count('id', filter=Q(status='refused')),
            pending=Count('id', filter=Q(status='pending')),
            aborted=Count('id', filter=Q(status='aborted'))
        )

        french_months = {
            1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril",
            5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août",
            9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
        }

        result = {french_months[month]: 0 for month in range(1, 13)}
        for entry in qs:
            month_name = french_months.get(entry['month'], str(entry['month']))
            result[month_name] = entry['total']


        payed_employees = Employee.objects.filter(
            user__is_active=True,
            payslips__month=now().month,
            payslips__year=now().year
        ).distinct().count()

        total_employees = Employee.objects.filter(user__is_active=True).count()
        unpayed_employees = total_employees - payed_employees

        inactifs = user_close.count()
        context["general"] ={
            "actif_users": users.count() - inactifs,
            "inactif_user": inactifs,
            "departemts": departement_cpt.count(),
            "employees": employee_cpt.count(),
            "hommes": genres.get('hommes', 0),
            "femmes": genres.get('femmes', 0),
            "disponible": users.count() - free - inactifs,
            "absent_today": employees_absent.count(),
            'absence_label': list(result.keys()),
            'absence_data': list(result.values()),
            'logged_in':logged_in,
            'conges_stats': {
                'accepted': qs2.get('accepted', 0),
                'refused': qs2.get('refused', 0),
                'pending': qs2.get('pending', 0),
                'aborted': qs2.get('aborted', 0)
            },
            'payments_stat' : {
            "payed": payed_employees,
            "unpayed": unpayed_employees
        }
        }
        context["prive"] = {
            "employees_added": employee_added.count(),
            "departement_added": departement_added.count(),
            "absences_personnel": absence
        }
        context['permissions'] = list(self.request.user.get_all_permissions())

        return context


@login_required
def dasbord_chart(request):
    me = request.user
    users = User.objects.all()
    # Get all non-expired sessions
    
    
    user_close = users.filter(is_active=False)
    departement_cpt = Departements.objects.all()
    employee_cpt = Employee.objects.all()
    employee_added = employee_cpt.filter(created_by = me)
    departement_added = departement_cpt.filter(created_by = me)
    free = User.objects.filter(is_active=True, profil_employee__conges__status=True).distinct().count()
    genres = User.objects.aggregate(
        hommes=Count('id', filter=Q(gender='masculin')),
        femmes=Count('id', filter=Q(gender='feminin'))
    )
    employees_absent = Presence.objects.filter(is_absent=True).filter(date=now().date()).distinct()

    # # Debug output for inspection
    # print("Genres dict:", genres)

    try:
        if me.profil_employee:
            absence = Presence.objects.filter(employee=me.profil_employee, is_absent=True).count()
    except Exception as e:
        # print("Exception in absence calculation:", e)
        absence = 0

    return JsonResponse({
    })
                    