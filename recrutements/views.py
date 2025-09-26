from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage 

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
            context = {
                "prenom": candidat.prenom,
                "nom": candidat.nom,
                "poste": offre.titre,
                "departement": offre.departement.name,
                "username": user.username,
                "password": password,
            }

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Félicitations - Candidature acceptée</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        background-color: #f8f9fa;
                        margin: 0;
                        padding: 20px;
                    }}
                    .email-container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background: white;
                        border-radius: 12px;
                        overflow: hidden;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                        color: white;
                        padding: 30px;
                        text-align: center;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 28px;
                    }}
                    .content {{
                        padding: 30px;
                    }}
                    .credentials-box {{
                        background: #f8f9fa;
                        border: 2px solid #28a745;
                        border-radius: 8px;
                        padding: 20px;
                        margin: 20px 0;
                    }}
                    .credentials-table {{
                        width: 100%;
                        margin: 15px 0;
                    }}
                    .credentials-table td {{
                        padding: 8px 0;
                        border-bottom: 1px solid #dee2e6;
                    }}
                    .credentials-table td:first-child {{
                        font-weight: bold;
                        width: 30%;
                    }}
                    .button {{
                        display: inline-block;
                        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
                        color: white;
                        padding: 15px 30px;
                        text-decoration: none;
                        border-radius: 25px;
                        font-weight: bold;
                        margin: 20px 0;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    }}
                    .warning {{
                        background: #fff3cd;
                        border: 1px solid #ffeaa7;
                        border-radius: 5px;
                        padding: 15px;
                        margin: 20px 0;
                        color: #856404;
                    }}
                    .footer {{
                        background: #343a40;
                        color: white;
                        text-align: center;
                        padding: 20px;
                        font-size: 14px;
                    }}
                    ul {{
                        padding-left: 20px;
                    }}
                    ul li {{
                        margin: 8px 0;
                    }}
                </style>
            </head>
            <body>
                <div class="email-container">
                    <div class="header">
                        <h1>🎉 Félicitations {context['prenom']} !</h1>
                        <p>Votre candidature a été acceptée</p>
                    </div>
                    
                    <div class="content">
                        <h2>Bonjour {context['prenom']} {context['nom']},</h2>
                        
                        <p>
                            Nous avons le plaisir de vous informer que vous avez été retenu(e) pour le poste de 
                            <strong>{context['poste']}</strong> dans le département <strong>{context['departement']}</strong>.
                        </p>
                        
                        <div class="credentials-box">
                            <h3 style="color: #28a745; margin-top: 0;">🔐 Vos identifiants de connexion</h3>
                            <p>Un compte RH a été créé pour vous :</p>
                            <table class="credentials-table">
                                <tr>
                                    <td><strong>Identifiant :</strong></td>
                                    <td>{context['username']}</td>
                                </tr>
                                <tr>
                                    <td><strong>Mot de passe :</strong></td>
                                    <td>{context['password']}</td>
                                </tr>
                            </table>
                        </div>
                        
                        <div class="warning">
                            <strong>⚠️ Important :</strong> Veuillez conserver ces informations en sécurité et ne les partagez avec personne.
                        </div>
                        
                        <p><strong>Prochaines étapes :</strong></p>
                        <ul>
                            <li>Connectez-vous à votre compte</li>
                            <li>Changez votre mot de passe lors de la première connexion</li>
                            <li>Complétez votre profil</li>
                            <li>Explorez les fonctionnalités disponibles</li>
                        </ul>
                        
                        <div style="text-align: center;">
                            <a href="https://ressourcesHumaines.onrender.com/login" class="button">
                                👉 Se connecter maintenant
                            </a>
                        </div>
                        
                        <p style="margin-top: 30px;">
                            Nous sommes ravis de vous accueillir dans notre équipe !
                        </p>
                    </div>
                    
                    <div class="footer">
                        <p><strong>L'équipe RH - Parinari</strong></p>
                        <p>© 2025 Parinari. Tous droits réservés.</p>
                        <p>Pour toute question, contactez-nous à parinari2025@gmail.com</p>
                    </div>
                </div>
            </body>
            </html>
            """
        
            from_email = EMAIL_HOST_USER
            to = [candidat.email]
        
            # Use EmailMultiAlternatives for both HTML and text versions
            email = EmailMessage(
                subject="🎉 Félicitations, vous avez été retenu(e) !",
                body=html_content,  # Plain text version
                from_email=from_email,
                to=to,
            )
            email.content_subtype = "html" 
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

