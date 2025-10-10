from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from comptabilite.models import Salary
from conges.models import CongesRequest, User
from departements.models import Departements
from employees.models import Employee
from presences.models import Abcence 
from django.db.models import Count
from django.db.models import Q
from django.db.models import Sum
from django.utils.timezone import now
from django.urls import reverse_lazy
from presences.models import Abcence
from django.db.models.functions import ExtractMonth
from django.contrib.sessions.models import Session
from django.utils import timezone
from recrutements.models import *
# Create your views here.

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth
from django.contrib.sessions.models import Session
from django.utils import timezone


class Dashboard(LoginRequiredMixin, View):
    """Dashboard view with staff and regular user views"""
    login_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        template = (
            'mainpage/dashbord.html' 
            if request.user.is_staff or request.user.is_superuser 
            else 'mainpage/dashbord_normal.html'
        )
        return render(request, template, self.get_context_data())

    def get_context_data(self, **kwargs):
        """Build context data for dashboard"""
        context = {}
        user = self.request.user
        
        # Personal statistics (available to all users)
        context["prive"] = self._get_private_context(user)
        
        # Admin statistics (only for staff/superuser)
        if user.is_staff or user.is_superuser:
            context["general"] = self._get_general_context()
            context["top_offres"] = self._get_top_offers_context()
            context["statuts"] = self._get_status_context()
            context["niveaux"] = self._get_level_context()
        
        context['permissions'] = list(user.get_all_permissions())
        
        return context

    def _get_private_context(self, user):
        """Get user-specific statistics"""
        # Move QuerySets outside to avoid NameError
        from .models import Employee, Departements, Abcence
        
        employee_added = Employee.objects.filter(created_by=user)
        departement_added = Departements.objects.filter(created_by=user)
        
        # Calculate personal absences
        absence_count = 0
        try:
            if hasattr(user, 'profil_employee') and user.profil_employee:
                absence_count = Abcence.objects.filter(
                    employee=user.profil_employee,
                    is_absent=True,
                    date__month=now().month,
                    date__year=now().year
                ).count()
        except (AttributeError, ObjectDoesNotExist):
            absence_count = 0
        
        return {
            "employees_added": employee_added.count(),
            "departement_added": departement_added.count(),
            "absences_personnel": absence_count
        }

    def _get_general_context(self):
        """Get general statistics for staff/admin"""
        from .models import (
            User, Departements, Employee, Abcence, 
            CongesRequest, Offre, Postulation
        )
        
        users = User.objects.select_related('profil_employee')
        inactive_users = users.filter(is_active=False)
        active_users = users.filter(is_active=True)
        
        departement_count = Departements.objects.count()
        employee_count = Employee.objects.count()
        
        # On leave today
        on_leave = User.objects.filter(
            is_active=True,
            profil_employee__conges__status=True
        ).distinct().count()
        
        # Gender distribution
        gender_stats = users.aggregate(
            hommes=Count('id', filter=Q(gender='masculin')),
            femmes=Count('id', filter=Q(gender='feminin'))
        )
        
        # Employees absent today
        today = now().date()
        present_ids = Abcence.objects.filter(date=today).values_list('employee_id', flat=True)
        
        employees_absent = Employee.objects.filter(
            date_embauche__lte=today,
            user__is_active=True
        ).exclude(id__in=present_ids).select_related('user')
        
        # Currently logged in users
        logged_in_count = self._get_logged_in_count()
        
        # Monthly absence statistics
        absence_by_month = self._get_monthly_absences()
        
        # Leave request statistics
        leave_stats = self._get_leave_statistics()
        
        # Payment statistics
        payment_stats = self._get_payment_statistics()
        
        return {
            "actif_users": active_users.count(),
            "inactif_user": inactive_users.count(),
            "departemts": departement_count,
            "employees": employee_count,
            "hommes": gender_stats.get('hommes', 0),
            "femmes": gender_stats.get('femmes', 0),
            "disponible": active_users.count() - on_leave,
            "absent_today": employees_absent.count(),
            'absence_label': absence_by_month['labels'],
            'absence_data': absence_by_month['data'],
            'logged_in': logged_in_count,
            'conges_stats': leave_stats,
            'payments_stat': payment_stats
        }

    def _get_logged_in_count(self):
        """Get count of currently logged in users"""
        from .models import User
        
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        uid_list = []
        
        for session in sessions:
            data = session.get_decoded()
            uid = data.get('_auth_user_id')
            if uid:
                uid_list.append(uid)
        
        return User.objects.filter(id__in=uid_list, is_active=True).count()

    def _get_monthly_absences(self):
        """Get absence statistics by month"""
        from .models import Abcence
        
        FRENCH_MONTHS = {
            1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril",
            5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août",
            9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
        }
        
        qs = Abcence.objects.filter(
            is_absent=True,
            date__year=now().year
        ).annotate(
            month=ExtractMonth('date')
        ).values('month').order_by('month').annotate(total=Count('id'))
        
        result = {FRENCH_MONTHS[month]: 0 for month in range(1, 13)}
        for entry in qs:
            month_name = FRENCH_MONTHS.get(entry['month'], str(entry['month']))
            result[month_name] = entry['total']
        
        return {
            'labels': list(result.keys()),
            'data': list(result.values())
        }

    def _get_leave_statistics(self):
        """Get leave request statistics"""
        from .models import CongesRequest
        
        stats = CongesRequest.objects.filter(
            created_at__year=now().year
        ).aggregate(
            accepted=Count('id', filter=Q(status='accepted')),
            refused=Count('id', filter=Q(status='refused')),
            pending=Count('id', filter=Q(status='pending')),
            aborted=Count('id', filter=Q(status='aborted'))
        )
        
        return {
            'accepted': stats.get('accepted', 0),
            'refused': stats.get('refused', 0),
            'pending': stats.get('pending', 0),
            'aborted': stats.get('aborted', 0)
        }

    def _get_payment_statistics(self):
        """Get payment statistics for current month"""
        from .models import Employee
        
        payed_employees = Employee.objects.filter(
            user__is_active=True,
            payslips__month=now().month,
            payslips__year=now().year
        ).distinct().count()
        
        total_employees = Employee.objects.filter(user__is_active=True).count()
        
        return {
            "payed": payed_employees,
            "unpayed": total_employees - payed_employees
        }

    def _get_top_offers_context(self):
        """Get top 5 job offers by postulation count"""
        from .models import Offre
        
        top_offres = Offre.objects.annotate(
            postulation_count=Count('postulations')
        ).order_by('-postulation_count')[:5]
        
        return {
            "labels": [offre.titre for offre in top_offres],
            "values": [offre.postulation_count for offre in top_offres]
        }

    def _get_status_context(self):
        """Get postulation status distribution"""
        from .models import Postulation
        
        statuts = Postulation.objects.values('statut').annotate(count=Count('id'))
        
        return {
            "labels": [statut['statut'] for statut in statuts],
            "values": [statut['count'] for statut in statuts]
        }

    def _get_level_context(self):
        """Get candidate level distribution"""
        from .models import Candidat
        
        niveaux = Candidat.objects.values('niveau').annotate(count=Count('id'))
        
        return {
            "labels": [niveau['niveau'] for niveau in niveaux],
            "values": [niveau['count'] for niveau in niveaux]
        }


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
    employees_absent = Abcence.objects.filter(is_absent=True).filter(date=now().date()).distinct()

    # # Debug output for inspection
    # print("Genres dict:", genres)

    try:
        if me.profil_employee:
            absence = Abcence.objects.filter(employee=me.profil_employee, is_absent=True).count()
    except Exception as e:
        # print("Exception in absence calculation:", e)
        absence = 0

    return JsonResponse({
    })
                    