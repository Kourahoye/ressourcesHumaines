from django.urls import path
from .views import PaimentCreateView, PaimentDeleteView, PaimentListView


urlpatterns = [
    path('create/',PaimentCreateView.as_view(), name='paiment_create'),
    path('list/', PaimentListView.as_view(), name='paiment_list'),
    path('delete/<int:pk>/', PaimentDeleteView.as_view(), name='paiment_delete'),
]