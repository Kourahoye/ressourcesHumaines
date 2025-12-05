from django.views import View
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import Attendance, Employee
import datetime

@method_decorator(csrf_exempt, name='dispatch')
class MarkAttendanceAjaxView(View):
    def post(self, request):
        try:
            employee_id = request.POST.get('employee_id')


            if not employee_id :
                return JsonResponse({'error': 'Selectionner un employer.'}, status=400)

            employee = get_object_or_404(Employee, id=employee_id)
            today = datetime.date.today()
            now_time = now().time()

            attendances, created = Attendance.objects.get_or_create(
                employee=employee,
                date=today,
            )

            if created :
                attendances.heure_arrivee = now_time()
                attendances.save()
                return JsonResponse({'message': f"Pointage enregistré avec succès."})
            if not created:
                attendances.heure_depart = now_time
                attendances.save()
                return JsonResponse({'message': f"Pointage enregistré avec succès."})
        except Exception as e:
            print(e)


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
