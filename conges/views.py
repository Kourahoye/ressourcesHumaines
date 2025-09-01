from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,DetailView,DeleteView
from conges.forms import CongeForm, CongeRequestForm
from .models import Conge, CongesRequest
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
# Create your views here.
 
class CongesRequestCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required =["conges.add_congesrequest"]
    login_url = reverse_lazy("login")
    model = CongesRequest
    form_class = CongeRequestForm
    template_name = "conges/requettes/create.html"
    success_url = reverse_lazy('conges_request_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
 

    def form_valid(self, form):
        
        form.instance.employee = self.request.user.profil_employee
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    

class CongesRequestList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required =["conges.list_congesrequest"]
    login_url = reverse_lazy("login")
    model = CongesRequest  
    template_name="conges/requettes/list.html"
    context_object_name ="congesRequests"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context



class CongesRequetsDelete(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    permission_required =["conges.delete_congesrequest"]
    login_url = reverse_lazy("login")
    model = CongesRequest
    template_name="conges/requettes/delete.html"
    success_url = reverse_lazy('conges_request_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context

class CongesRequestDetails(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    permission_required =["conges.view_congesrequest"]
    login_url = reverse_lazy("login")
    model = CongesRequest
    template_name="conges/requettes/details.html"

@login_required(login_url='login')
@permission_required(['conges.accept_congesrequest'])
def acceptRequest(request,pk):
    requette = CongesRequest.objects.get(pk=pk)
    requette.status = 'accepted'
    requette.save()

    conges = Conge()
    conges.employee = request.user.profil_employee
    conges.startDate = requette.startDate
    conges.endDate = requette.endDate
    conges.created_by = request.user
    conges.updated_by = request.user
    conges.save()
    return redirect(reverse_lazy('conges_request_list'))

# @login_required(login_url='login')
@permission_required(['conges.refuse_congesrequest'])
def refuseRequest(request,pk):
    requette = CongesRequest.objects.get(pk=pk)
    requette.status = 'refused'
    requette.save()
    return redirect(reverse_lazy('conges_request_list'))

@login_required(login_url='login')
@permission_required(['conges.change_conge_status'])
def finishConges(request,pk):
    conge = Conge.objects.get(pk=pk)
    conge.status = True
    conge.save()
    return redirect(reverse_lazy('conges_list'))

@login_required(login_url='login')
@permission_required(['conges.change_conge_status'])
def unfinishConges(request,pk):
    conge = Conge.objects.get(pk=pk)
    conge.status = False
    conge.save()
    return redirect(reverse_lazy('conges_list'))

@login_required(login_url='login')
@permission_required(['conges.delete_conges'])
def deleteConges(request,pk):
    conge = Conge.objects.get(pk=pk)
    conge.delete()
    return redirect(reverse_lazy('conges_list'))



class CongesList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required =["conges.list_conge"]
    login_url = reverse_lazy("login")
    model = Conge
    context_object_name = 'conges'
    template_name="conges/conges/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
    

class CongesCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    permission_required =["conges.add_conges"]
    login_url = reverse_lazy("login")
    model = Conge
    template_name = "conges/conges/create.html"
    success_url = reverse_lazy('conges_request_list')
    form_class = CongeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
