from django.urls import path
from .views import DepartementAssign, DepartementHeadDeleteView, DepartementHeadsListView, DepartementsCreateView, DepartementsDeleteView, DepartementsDetailView, DepartementsListView, DepartementsUpdateView, desativate_departement_head, load_employees

urlpatterns = [
    path('add/', DepartementsCreateView.as_view(), name='departement_add'),
    path('', DepartementsListView.as_view(), name='liste_departements'),
    path('delete/<int:pk>/',DepartementsDeleteView.as_view(),name='departements_delete'),
    path('profil/<int:pk>/',DepartementsDetailView.as_view(),name='departements_profil'),
    path('update/<int:pk>/',DepartementsUpdateView.as_view(),name='departements_update'),
    path('assign-head/',DepartementAssign.as_view(),name='departements_assign_head'),
    path('heads/',DepartementHeadsListView.as_view(),name='departements_list_head'),
    path('load-employees/', load_employees, name='ajax_load_employees'),
    path('head/remove/<int:pk>/',DepartementHeadDeleteView.as_view(),name='departement_head_delete'),
    path('head/desactive/<int:pk>/',desativate_departement_head, name='departement_head_desactive'),
]
