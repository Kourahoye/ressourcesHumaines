# urls.py
from django.urls import path

from .views import PresenceList, presence_page, presences_data


urlpatterns = [
    path('', presence_page, name='presence_page'),
    path('api/presences/', presences_data, name='api_presences'),
    path('absences/', PresenceList.as_view(), name='subor_presences'),
]
