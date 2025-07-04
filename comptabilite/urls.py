from django.urls import path
from .views import BonusCreateView, BonusDeleteView, BonusListView, PaimentCreateView, PaimentDeleteView, PaimentListView, PaimentUpdateView,PayEmployeeView, PaymentList,PayslipDetailView,PayslipDeleteView,BonusDetailsView


urlpatterns = [
    path('salary/create/',PaimentCreateView.as_view(), name='salary_create'),
    path('salaries/', PaimentListView.as_view(), name='salary_list'),
    path('salary/delete/<int:pk>/', PaimentDeleteView.as_view(), name='salary_delete'),
    path('salary/update/<int:pk>/', PaimentUpdateView.as_view(), name='salary_update'),
    path('primes/create/',BonusCreateView.as_view(), name='bonus_create'),
    path('primes/', BonusListView.as_view(), name='bonus_list'),
    path('primes/delete/<int:pk>/', BonusDeleteView.as_view(), name='bonus_delete'),
    path('primes/<int:pk>/', BonusDetailsView.as_view(), name='bonus_details'),
    path('paiment/create/', PayEmployeeView.as_view(), name='paiment_salary'),
    path('', PaymentList.as_view(), name='paiment_salary_list'),
    path('paiments/<int:pk>/', PayslipDetailView.as_view(), name='payslip_detail'),
    path('paiments/delete/<int:pk>/', PayslipDeleteView.as_view(), name='payslip_delete'),
]