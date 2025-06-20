# views.py
from django.utils import timezone
from datetime import date as DATE
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.timezone import now
from .models import Presence
from employees.models import Employee
import json
from django.views.generic import ListView

@login_required
def presence_page(request):
    context = {
        'permissions':list(request.user.get_all_permissions()),
        'today':timezone.now()
    }
    return render(request, 'presences/rapport_add.html',context=context)

@csrf_exempt
@login_required
def presences_data(request):
    if request.method == 'GET':
        date_str = request.GET.get('date', str(now().date()))
        date2 = DATE.fromisoformat(date_str)

        if date2 > DATE.today():
            return JsonResponse({'error': True, "message": "La date ne doit pas être dans le futur"})

        employees = Employee.objects.all()
        presences = Presence.objects.filter(date=date2)
        presence_map = {p.employee_id: p for p in presences}

        # Liste des nouvelles présences à créer (présence absente => créer avec is_absent=False)
        new_presences = [
            Presence(employee=emp, date=date2, is_absent=False,created_by=request.user)
            for emp in employees
            if emp.id not in presence_map
        ]

        if new_presences:
            Presence.objects.bulk_create(new_presences)

            # Recharger les présences après insertion
            presences = Presence.objects.filter(date=date2)
            presence_map = {p.employee_id: p for p in presences}

        # Préparer les données pour la réponse
        data = [
            {
                'employee_id': emp.id,
                'employee_name': str(emp.user),
                'is_absent': presence_map[emp.id].is_absent
            }
            for emp in employees
        ]

        return JsonResponse({'presences': data})

    if request.method == 'POST':
        payload = json.loads(request.body)
        emp_id = payload['employee_id']
        date = payload['date']
        is_absent = payload.get('is_absent', False)
        user = request.user

        presence, created = Presence.objects.update_or_create(
            employee_id=emp_id,
            date=date,
            defaults={
                'is_absent': is_absent,
                'created_by': user
            }
        )
        return JsonResponse({'success': True})


class PresenceList(ListView):
    model = Presence
    context_object_name = 'absences'
    template_name='presences/absences.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context

    def get_queryset(self):
        from django.db.models import Q
        if self.request.user.is_superuser or self.request.user.is_staff:
            queryset = Presence.objects.all().filter(is_absent=True).order_by("-date","employee__user")
        else:
            queryset = Presence.objects.filter(employee__manager = self.request.user.profil_employee,isis_absent=True).order_by("-date","employee__user")
        return queryset