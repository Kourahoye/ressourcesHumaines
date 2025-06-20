from django.urls import path
from .views import DepartementsCreateView, DepartementsDeleteView, DepartementsDetailView, DepartementsListView, DepartementsUpdateView

urlpatterns = [
    path('add/', DepartementsCreateView.as_view(), name='departement_add'),
    path('', DepartementsListView.as_view(), name='liste_departements'),
    path('delete/<int:pk>/',DepartementsDeleteView.as_view(),name='departements_delete'),
    path('profil/<int:pk>/',DepartementsDetailView.as_view(),name='departements_profil'),
    path('update/<int:pk>/',DepartementsUpdateView.as_view(),name='departements_update'),
 
]
