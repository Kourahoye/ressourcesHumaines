from django.shortcuts import render
from django.views.generic.edit import CreateView
from employees.models import Employee
from .forms import OffreForm, PostulationAdminForm
from .models import Offre
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Offre, Candidat, Postulation
from .forms import CandidatForm, PostulationForm


# Create your views here.
class OffreCreateView(CreateView):
    model = Offre
    form_class = OffreForm
    template_name = 'recrutements/offres/create.html'
    success_url = reverse_lazy('offre-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)



class OffreUpdateView(UpdateView):
    model = Offre
    form_class = OffreForm
    template_name = 'recrutements/offres/update.html'
    success_url = reverse_lazy('offre-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class OffreListView(ListView):
    model = Offre
    template_name = 'recrutements/offres/list.html'
    context_object_name = 'offres'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context

# views.py


class PostulerOffreView(View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
    def get(self, request, offre_id):
        offre = get_object_or_404(Offre, id=offre_id)
        form_candidat = CandidatForm()
        form_postulation = PostulationForm()
        return render(request, 'recrutements/candidatures/postulation.html', {
            'offre': offre,
            'form_candidat': form_candidat,
            'form_postulation': form_postulation,
        })

    def post(self, request, offre_id):
        offre = get_object_or_404(Offre, id=offre_id)
        form_candidat = CandidatForm(request.POST, request.FILES)
        form_postulation = PostulationForm(request.POST)

        if form_candidat.is_valid() and form_postulation.is_valid():
            candidat = form_candidat.save()

            if Postulation.objects.filter(candidat=candidat, offre=offre).exists():
                return JsonResponse({'candidat': {'email': ['Vous avez déjà postulé.']}}, status=400)

            postulation = form_postulation.save(commit=False)
            postulation.candidat = candidat
            postulation.offre = offre
            postulation.save()

            return JsonResponse({'success': 'Postulation enregistrée avec succès !'})

        return JsonResponse({
            'candidat': form_candidat.errors,
            'postulation': form_postulation.errors
        }, status=400)
    
from django.views.generic import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Postulation

class PostulationListView(PermissionRequiredMixin, ListView):
    model = Postulation
    template_name = 'recrutements/candidatures/list.html'  # adapte selon ton arborescence
    context_object_name = 'postulations'
    paginate_by = 10
    permission_required = 'recrutements.list_postulation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
    def get_queryset(self):
        # Optionnel : filtre par utilisateur ou autres critères
        qs = super().get_queryset().select_related('candidat', 'offre', 'offre__departement')
        return qs.order_by('-date_postulation')

from django.views.generic.edit import UpdateView
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.crypto import get_random_string


User = get_user_model()

class PostulationDetailView(UpdateView):
    model = Postulation
    form_class = PostulationAdminForm
    template_name = 'recrutements/candidatures/details.html'
    context_object_name = 'postulation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
    def get_success_url(self):
        return reverse_lazy('postulation_detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        old_statut = self.object.statut

        form = self.get_form()
        if form.is_valid():
            self.object = form.save()
            new_statut = self.object.statut

            if old_statut != 'accepte' and new_statut == 'accepte':
                self.create_user_and_employee(self.object)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def create_user_and_employee(self, postulation):
        candidat = postulation.candidat
        offre = postulation.offre

        # Créer un username unique
        username = self.generate_username(candidat)

        # Créer ou récupérer un utilisateur
        password = get_random_string(10)

        user, created = User.objects.get_or_create(
            email=candidat.email,
            defaults={
                'username': username,
                'first_name': candidat.prenom,
                'last_name': candidat.nom,
                'gender': candidat.genre,
                'birthday': candidat.date_naissance,
                'avatar': 'avatars/default.jpg',
            }
        )
        # print("==========================")
        if  created:
            user.set_password(password)
            user.save()
            # print("==========================")
            # # Envoi d'email simulé dans la console
            # print("📧 Envoi email à :", user.email)
            send_mail(
                subject="🎉 Félicitations, vous avez été retenu(e) !",
                message=f"""
                    Bonjour {candidat.prenom},

                    Félicitations ! Vous avez été retenu(e) pour le poste de "{offre.titre}" dans le département {offre.departement.name}.

                    Votre compte RH a été créé :
                    Identifiant : {user.username}
                    Mot de passe : {password}

                    Cordialement,
                    RH
                    """,
                from_email="noreply@entreprise.com",
                recipient_list=[user.email],
                fail_silently=False,
            )

        # Créer un employé s’il n’existe pas déjà
        if not hasattr(user, 'profil_employee'):
            Employee.objects.create(
                user=user,
                poste=offre.titre,
                departement=offre.departement,
                date_embauche=timezone.now().date(),
                created_by=self.request.user,
            )
            # print("=========================")

    def generate_username(self, candidat):
        base = slugify(f"{candidat.prenom}-{candidat.nom}")
        username = base
        counter = 1
        while User.objects.filter(username=username).exists():
            counter += 1
            username = f"{base}{counter}"
        return username
    # print("===============END==============")
