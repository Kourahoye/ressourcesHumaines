from django.urls import path
from .views import PaimentCreateView, PaimentListView


urlpatterns = [
    path('create/',PaimentCreateView.as_view(), name='paiment_create'),
    path('list/', PaimentListView.as_view(), name='paiment_list'),
]