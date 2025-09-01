from django.urls import path

from attendances.views import AttendanceView, MarkAttendanceAjaxView, PresencesTodayAjaxView


urlpatterns = [
    path('mark/', MarkAttendanceAjaxView.as_view(), name='mark_attendance'),
    path('today/', PresencesTodayAjaxView.as_view(), name='PresencesToday'),
    path('', AttendanceView.as_view(), name='attendances'),
]