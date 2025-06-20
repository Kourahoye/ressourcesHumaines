from django.urls import path

from .views import ClassementDepartement, ClassementEmployee, DepartementRatingCreateView, DepartementRatingList, EmployeeRatingCreateView, EmployeeRatingList

urlpatterns = [
    path('departements/create',DepartementRatingCreateView.as_view(),name="note_departement"),
    path('departements/',DepartementRatingList.as_view(),name="departements_notes"),
    path('employees/create',EmployeeRatingCreateView.as_view(),name="note_employee"),
    path('employees/',EmployeeRatingList.as_view(),name="employees_notes"),
    path('classement/employees/',ClassementEmployee.as_view(),name="classement_employees"),
    path('classement/departements/',ClassementDepartement.as_view(),name="classement_departement"),
]
