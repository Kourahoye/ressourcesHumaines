from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,UpdateView,FormView,DetailView,DeleteView
from .models import   BonusSlip, Payslip, Salary
from .forms import BonusSlipForm, SalaryForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin as PermissionsRequiredMixins
from django.contrib import messages
from .forms import PaimentForm
from .models import Payslip, Salary

# Create your views here.
class PaimentCreateView(LoginRequiredMixin,PermissionsRequiredMixins,CreateView):
    permission_required =['comptabilite.add_paiment']
    model = Salary
    form_class = SalaryForm
    template_name = 'comptabilite/salary/create.html'
    success_url = reverse_lazy('salary_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = self.request.user.get_all_permissions()
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class PaimentUpdateView(LoginRequiredMixin,PermissionsRequiredMixins,UpdateView):
    permission_required =['comptabilite.change_paiment']
    model = Salary
    form_class = SalaryForm
    template_name = 'comptabilite/salary/create.html'
    success_url = reverse_lazy('salary_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = self.request.user.get_all_permissions()
        return context
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    

class PaimentListView(LoginRequiredMixin,PermissionsRequiredMixins,ListView):
    permission_required =['comptabilite.list_paiment']
    model = Salary
    template_name = 'comptabilite/salary/list.html'
    context_object_name = 'paiments'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = self.request.user.get_all_permissions()
        return context
    

class PaimentDeleteView(LoginRequiredMixin,PermissionsRequiredMixins,CreateView):
    permission_required =['comptabilite.delete_paiment']
    model = Salary
    template_name = 'comptabilite/salary/delete.html'
    success_url = reverse_lazy('salary_list')
    context_object_name = 'paiment'
    form_class = SalaryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = self.request.user.get_all_permissions()
        return context

    def post(self, request, *args, **kwargs):

        paiment = self.get_object()
        if paiment:
            paiment.delete()
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)


class BonusCreateView(LoginRequiredMixin,PermissionsRequiredMixins,CreateView):
    permission_required =['comptabilite.add_bonus']
    model = BonusSlip
    form_class = BonusSlipForm
    template_name = 'comptabilite/bonus/create.html'
    success_url = reverse_lazy('bonus_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = self.request.user.get_all_permissions()
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        date = form.cleaned_data.get('date')
        # print(date)
        form.instance.month = date.month
        form.instance.year = date.year
        return super().form_valid(form)


class BonusDetailsView(LoginRequiredMixin,PermissionsRequiredMixins,DetailView):
    permission_required =['comptabilite.view_bonus']
    model = BonusSlip
    template_name = 'comptabilite/bonus/details.html'
    success_url = reverse_lazy('bonus_list')
    context_object_name ='payslip'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = self.request.user.get_all_permissions()
        return context
     

class BonusListView(LoginRequiredMixin,PermissionsRequiredMixins,ListView):
    permission_required =['comptabilite.list_bonus']
    model = BonusSlip
    template_name = 'comptabilite/bonus/list.html'
    context_object_name = 'paiments'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = self.request.user.get_all_permissions()
        return context
    

class BonusDeleteView(LoginRequiredMixin,PermissionsRequiredMixins,CreateView):
    permission_required =['comptabilite.delete_bonus']
    model = BonusSlip
    template_name = 'comptabilite/bonus/delete.html'
    success_url = reverse_lazy('bonus_list')
    context_object_name = 'paiment'
    form_class = BonusSlipForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = self.request.user.get_all_permissions()
        return context

    def post(self, request, *args, **kwargs):

        paiment = self.get_object()
        if paiment:
            paiment.delete()
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
    

class PayEmployeeView(LoginRequiredMixin, PermissionsRequiredMixins, CreateView):
    template_name = 'comptabilite/paiments/create.html'
    form_class = PaimentForm
    success_url = reverse_lazy('paiment_salary_list')
    permission_required = ['comptabilite.add_payslip']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = self.request.user.get_all_permissions()
        return context

    def form_valid(self, form):
        employee = form.instance.employee
        date = form.cleaned_data.get('date')
        month, year = date.month, date.year
        try:
            salary = Salary.objects.get(employee=employee)
        except Salary.DoesNotExist:
            form.add_error(None, "Salaire introuvable pour cet employé.")
            return self.form_invalid(form)


        if Payslip.objects.filter(employee=employee, month=month, year=year).exists():
            form.add_error(None, "Une fiche de paie pour ce mois existe déjà.")
            return self.form_invalid(form)

        form.instance.generated_by= self.request.user
        form.instance.base_salary = employee.salary.amount
        form.instance.month = month
        form.instance.year = year
        return super().form_valid(form)

class PaymentList(LoginRequiredMixin, PermissionsRequiredMixins,ListView):
    model = Payslip
    permission_required =['comptabilite.list_payslip']
    template_name = 'comptabilite/paiments/list.html'
    context_object_name = 'paiments'
    paginate_by = 5 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = self.request.user.get_all_permissions()
        return context
    
class PayslipDetailView(LoginRequiredMixin, PermissionsRequiredMixins, DetailView):
    model = Payslip
    template_name = 'comptabilite/paiments/details.html'  # crée ce template
    context_object_name = 'payslip'
    permission_required = ['comptabilite.view_payslip']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = self.request.user.get_all_permissions()
        return context


class PayslipDeleteView(DeleteView):
    model = Payslip
    template_name =  'comptabilite/paiments/delete.html'
    success_url = reverse_lazy('paiment_salary_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = self.request.user.get_all_permissions()
        return context

    def post(self, request, *args, **kwargs):

        paiment = self.get_object()
        if paiment:
            paiment.delete()
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)