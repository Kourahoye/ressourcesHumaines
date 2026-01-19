from typing import Any
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import  redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView,FormView,DetailView,UpdateView,ListView,DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from Users.forms import CustomPasswordChangeForm, RegisterForm,LoginForm, UserUpdateForm
from Users.models import  User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.shortcuts import render
from django import forms
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import redirect



# Create your views here.
class RegisterView(PermissionRequiredMixin,CreateView):
    permission_required =['Users.add_user']
    model = User
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy('dashbord')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)
    def form_valid(self, form) -> HttpResponse:       
        form.instance.password =  make_password(form.cleaned_data['password'])
        form.instance.is_active = False
        form.instance.must_change_password = True
        return super().form_valid(form)


class UserupdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required =['Users.change_user']
    login_url = 'login'
    model = User
    form_class = UserUpdateForm
    template_name = "users/update.html"
    success_url = reverse_lazy('dashbord')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        #print(user)
        if self.request.POST['password']:
            user = authenticate(username=self.request.user.username,password=self.request.POST['password'])
            #print(self.request.user.pk)
            if user:
                form.save()
                return super().form_valid(form)
            return render(self.request,'users/update.html',{'form':form,'error':'Mot de passe incorecte'})
        return render(self.request,'users/update.html',{'form':form,'error':'Mot de passe obligatoire'})

class LoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("dashbord")
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        username = request.POST.get("username")
        password= request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user:
            login(request, user)
            return redirect('dashbord')
        return render(request,'users/login.html',{'form':LoginForm,'error':'Nom d\'user ou mot de passe incorecte'})

def Logout(request):
    logout(request)
    return redirect('login')


class UserDetailView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    permission_required =['Users.view_user']
    login_url ='login'
    model = User
    template_name = "users/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
    
class UserList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ['Users.list_users']
    model = User
    context_object_name = 'users'
    template_name = "users/list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        uid_list = []
        for session in sessions:
            data = session.get_decoded()
            uid = data.get('_auth_user_id')
            if uid:
                uid_list.append(int(uid))

        online_user_ids = set(uid_list)

        for user in queryset:
            user.online = user.id in online_user_ids

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
    



class UserDeleteForm(forms.Form):
    # formulaire vide, juste pour gérer l'erreur
    pass

class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('user-list')
    template_name = 'users/delete.html'  # ton template delete

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user and not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # afficher le formulaire vide (confirmation)
        form = UserDeleteForm()
        return render(request, self.template_name, {'object': self.get_object(), 'form': form})

    def post(self, request, *args, **kwargs):
        form = UserDeleteForm(request.POST)
        if not form.is_valid():
            # jamais arrivé car pas de champs, mais à titre d'exemple
            return self.form_invalid(form)

        user = self.get_object()
        relations_bloquantes = []

        for rel in user._meta.related_objects:
            accessor_name = rel.get_accessor_name()
            related_manager = getattr(user, accessor_name)
            try:
                if rel.one_to_one:
                    if related_manager is not None:
                        relations_bloquantes.append(f"{rel.related_model.__name__} (OneToOne)")
                elif rel.one_to_many:
                    if related_manager.exists():
                        relations_bloquantes.append(f"{rel.related_model.__name__} (ForeignKey)")
                elif rel.many_to_many:
                    if related_manager.exists():
                        relations_bloquantes.append(f"{rel.related_model.__name__} (ManyToMany)")
            except Exception:
                continue

        if relations_bloquantes:
            form.add_error(None, ValidationError(
                "Suppression interdite : utilisateur a effectuer des actions" #+ ", ".join(relations_bloquantes)
            ))
            user.is_active = False
            user.save()
            form.add_error(None, ValidationError(
                "Utilisateur desactivé" #+ ", ".join(relations_bloquantes)
            ))
            return self.form_invalid(form)

        # pas de relations bloquantes, suppression normale
        return self.delete(request, *args, **kwargs)

    def form_invalid(self, form):
        # afficher le template avec erreurs
        return render(self.request, self.template_name, {'form': form, 'object': self.get_object()})


@login_required
@permission_required('Users.change_user',raise_exception=True)
def toggle_user_active(request, user_id):

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "Utilisateur non trouvé.")
        referrer = request.META.get('HTTP_REFERER')
        return redirect(referrer) if referrer else redirect('user-list')

    if user == request.user:
        messages.error(request, "Vous ne pouvez pas désactiver votre propre compte.")
        referrer = request.META.get('HTTP_REFERER')
        return redirect(referrer) if referrer else redirect('user-list')

    user.is_active = not user.is_active
    user.must_change_password = True
    user.save()
    status = "activé" if user.is_active else "désactivé"
    messages.success(request, f"Utilisateur {user.username} {status}.")
    referrer = request.META.get('HTTP_REFERER')
    return redirect(referrer) if referrer else redirect('user-list')


from django.contrib.auth import update_session_auth_hash
from django.views.generic import FormView

class change_password(FormView,LoginRequiredMixin,PermissionRequiredMixin):
    permission_required =['Users.change_user']
    login_url = 'login'
    form_class = CustomPasswordChangeForm
    template_name = "users/change_password.html"
    success_url = reverse_lazy('dashbord')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data['new_password1'])
        if hasattr(user, 'must_change_password'):
            user.must_change_password = False
        user.save()
        update_session_auth_hash(self.request, user)  # garde l'utilisateur connecté
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs.")
        return super().form_invalid(form)
