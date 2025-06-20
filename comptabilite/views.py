from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView
from .models import Paiment
from .forms import PaimentForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin as PermissionsRequiredMixins

# Create your views here.
class PaimentCreateView(LoginRequiredMixin,PermissionsRequiredMixins,CreateView):
    permission_required =['comptabilite.add_paiment']
    model = Paiment
    form_class = PaimentForm
    template_name = 'comptabilite/create.html'
    success_url = reverse_lazy('paiment_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = self.request.user.get_all_permissions()
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    

class PaimentListView(LoginRequiredMixin,PermissionsRequiredMixins,ListView):
    permission_required =['comptabilite.list_paiment']
    model = Paiment
    template_name = 'comptabilite/list.html'
    context_object_name = 'paiments'
    paginate_by = 10  # Nombre d'objets par page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = self.request.user.get_all_permissions()
        return context
    

class PaimentDeleteView(LoginRequiredMixin,PermissionsRequiredMixins,CreateView):
    permission_required =['comptabilite.delete_paiment']
    model = Paiment
    template_name = 'comptabilite/delete.html'
    success_url = reverse_lazy('paiment_list')
    context_object_name = 'paiment'
    form_class = PaimentForm

    def post(self, request, *args, **kwargs):

        paiment = self.get_object()
        if paiment:
            paiment.delete()
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)