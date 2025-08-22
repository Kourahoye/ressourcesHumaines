from django.views import View
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.urls import path
from django.core.serializers import serialize
from django.forms.models import model_to_dict
from django.views.generic import TemplateView
from .models import Attendance, Employee
import datetime

@method_decorator(csrf_exempt, name='dispatch')
class MarkAttendanceAjaxView(View):
    def post(self, request):
        employee_id = request.POST.get('employee_id')
        action = request.POST.get('action')

        if not employee_id or action not in ['arrivee', 'depart']:
            return JsonResponse({'error': 'Données invalides.'}, status=400)

        employee = get_object_or_404(Employee, id=employee_id)
        today = datetime.date.today()

        attendances, created = Attendance.objects.get_or_create(
            employee=employee,
            date=today,
            defaults={'heure_arrivee': None, 'heure_depart': None}
        )

        now_time = now().time()

        if action == 'arrivee':
            if attendances.heure_arrivee:
                return JsonResponse({'error': "L'arrivée a déjà été enregistrée."}, status=400)
            attendances.heure_arrivee = now_time
        elif action == 'depart':
            if attendances.heure_depart:
                return JsonResponse({'error': "Le départ a déjà été enregistré."}, status=400)
            attendances.heure_depart = now_time

        attendances.save()
        return JsonResponse({'message': f"Pointage '{action}' enregistré avec succès."})


@method_decorator(csrf_exempt, name='dispatch')
class PresencesTodayAjaxView(View):
    def get(self, request):
        today = datetime.date.today()
        attendancess = Attendance.objects.filter(date=today).select_related('employee__user')

        data = [
            {
                'employee': p.employee.user.get_full_name(),
                'heure_arrivee': p.heure_arrivee.strftime('%H:%M') if p.heure_arrivee else '-',
                'heure_depart': p.heure_depart.strftime('%H:%M') if p.heure_depart else '-',
            }
            for p in attendancess
        ]
        return JsonResponse({'Attendancess': data})


class AttendanceView(TemplateView):
    template_name = "attendances/suivi.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        context['employees'] = Employee.objects.all().filter(user__is_active = True)
        context['today'] = now()
        return context
