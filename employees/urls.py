from django.urls import path
from .views import EmployeeCreateView, EmployeeDeleteView,EmployeeListView,EmployeeDetailView,EmployeeUpdateView

urlpatterns = [
    path('add/', EmployeeCreateView.as_view(), name='employee_add'),
    path('', EmployeeListView.as_view(), name='employee_list'),
    path('delete/<int:pk>/',EmployeeDeleteView.as_view(),name='employee_delete'),
    path('profil/<int:pk>/',EmployeeDetailView.as_view(),name='employee_profil'),
    path('update/<int:pk>/',EmployeeUpdateView.as_view(),name='employee_update'),
]
