from django.urls import path
from .views import Dasbord, dasbord_chart
urlpatterns = [
    path('',Dasbord.as_view(),name='dashbord'),
    path('chart/',dasbord_chart,name='chart'),
]