# Django core
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from django.utils.crypto import get_random_string

# Generic class-based views
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

# Models
from employees.models import Employee
from ressourcesHumaines.settings import EMAIL_HOST_USER
from .models import Offre, Postulation

# Forms
from .forms import (
    OffreForm,
    PostulationAdminForm,
    CandidatForm,
    PostulationForm
)

# Python standard
from datetime import datetime

User = get_user_model()

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
        form.instance.acitve = True
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)




class DeleteOffreView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Offre
    template_name = 'recrutements/offres/delete.html'
    success_url = reverse_lazy('offre-list')
    success_message = "L'offre a été supprimée avec succès"

    def test_func(self):
        """Vérifie que l'utilisateur a le droit de supprimer l'offre"""
        offre = self.get_object()
        return (
            self.request.user.is_superuser or 
            self.request.user == offre.created_by or
            self.request.user.has_perm('recrutements.delete_offre')
        )

    def get_context_data(self, **kwargs):
        """Ajoute des informations supplémentaires au contexte"""
        context = super().get_context_data(**kwargs)
        context['title'] = "Confirmer la suppression"
        return context

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




from datetime import date, datetime, time
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import Http404

class PostulerOffreView(View):
    def get(self, request, offre_id):
        # Récupération de l'offre ou 404
        offre = get_object_or_404(Offre, id=offre_id)

        # Normalisation date_expiration en datetime
        if isinstance(offre.date_expiration, date) and not isinstance(offre.date_expiration, datetime):
            date_exp = timezone.make_aware(datetime.combine(offre.date_expiration, time.min))
        else:
            date_exp = offre.date_expiration

        # Vérification de disponibilité
        if not offre.active or date_exp < timezone.now():
            raise Http404("Cette offre n'est plus disponible")

        # Préparation des formulaires
        form_candidat = CandidatForm()
        form_postulation = PostulationForm()

        # Calcul du temps restant
        maintenant = timezone.now()
        temps_restant = date_exp - maintenant
        jours = temps_restant.days
        secondes_restantes = temps_restant.seconds
        heures, reste = divmod(secondes_restantes, 3600)
        minutes, secondes = divmod(reste, 60)

        return render(request, 'recrutements/candidatures/postulation.html', {
            'offre': offre,
            'form_candidat': form_candidat,
            'form_postulation': form_postulation,
            'jours': jours,
            'heures': heures,
            'minutes': minutes,
            'secondes': secondes,
            'date_expiration_iso': date_exp.isoformat(),
        })


    def post(self, request, offre_id):
        offre = get_object_or_404(Offre, id=offre_id)
        form_candidat = CandidatForm(request.POST, request.FILES)
        form_postulation = PostulationForm(request.POST)

        if form_candidat.is_valid() and form_postulation.is_valid():
            candidat = form_candidat.save()

            # Vérifie si ce candidat a déjà postulé
            if Postulation.objects.filter(candidat=candidat, offre=offre).exists():
                return JsonResponse({'candidat': {'email': ['Vous avez déjà postulé.']}}, status=400)

            # Enregistre la postulation
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

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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

        # Générer un mot de passe aléatoire
        password = get_random_string(10)

        # Créer ou récupérer un utilisateur
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

        if created:
            user.set_password(password)
            user.save()

            # Préparer le contenu email (HTML + texte)
            context = {
                "prenom": candidat.prenom,
                "nom": candidat.nom,
                "poste": offre.titre,
                "departement": offre.departement.name,
                "username": user.username,
                "password": password,
            }

            html_content = render_to_string("recrutements/emails/acceptation.html", context)
            text_content = strip_tags(html_content)  # version texte brut
 
            email = EmailMultiAlternatives(
                subject="🎉 Félicitations, vous avez été retenu(e) !",
                body=text_content,
                from_email= EMAIL_HOST_USER,
                to=[user.email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

        # Créer un employé s’il n’existe pas déjà
        if not hasattr(user, 'profil_employee'):
            Employee.objects.create(
                user=user,
                poste=offre.titre,
                departement=offre.departement,
                date_embauche=timezone.now().date(),
                created_by=self.request.user,
            )

    def generate_username(self, candidat):
        base = slugify(f"{candidat.prenom}-{candidat.nom}")
        username = base
        counter = 1
        while User.objects.filter(username=username).exists():
            counter += 1
            username = f"{base}{counter}"
        return username

