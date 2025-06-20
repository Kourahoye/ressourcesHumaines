from typing import Any
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import  redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView,FormView,DetailView,UpdateView,ListView

from Users.forms import RegisterForm,LoginForm, UserUpdateForm
from Users.models import  User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth.hashers import make_password




# Create your views here.
class RegisterView(CreateView):
    # permission_required =['users.add_user']
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
                # up_form = form.save(commit=False)
                # up_form.password = make_password(form.cleaned_data['password'])
                # up_form.save()
                # user = authenticate(username=self.request.POST['username'], password=self.request.POST['password'])
                # if(up_form):
                #      login(self.request, user)
                #     return redirect('login')            
        form.instance.password =  make_password(form.cleaned_data['password'])
        form.instance.is_active = False
        return super().form_valid(form)


class UserupdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    permission_required =['users.change_user']
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
    permission_required =['users.view_user']
    login_url ='login'
    model = User
    template_name = "users/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
    
class UserList(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required =['users.list_users']
    model = User
    context_object_name = 'users'
    template_name="users/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context