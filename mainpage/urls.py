from django.urls import path
from .views import Dasboard
urlpatterns = [
    path('',Dasboard.as_view(),name='dashbord'),
]