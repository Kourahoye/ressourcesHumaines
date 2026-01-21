# views.py
import bleach
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from Users.models import User
from departements.models import Departements
from employees.models import Employee
from .forms import MessageForm
from .models import Message, Notification
from django.views.generic import FormView
# from .models import Message, MessageRecipient

from bleach.css_sanitizer import CSSSanitizer

ALLOWED_CSS_PROPERTIES = [
    'color',
    'background-color',
    'font-size',
    'font-family',
    'font-weight',
    'text-align',
    'text-decoration',
    'border',
    'border-color',
    'border-width',
    'padding',
    'margin',
]

ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS.union([
    # Texte de base
    'p', 'br', 'span', 'hr',

    # Titres
    'h1', 'h2', 'h3',

    # Mise en forme
    'strong', 'em', 'u', 's',
    'sub', 'sup', 'mark',
    'code', 'pre',

    # Listes
    'ul', 'ol', 'li',

    # Citations
    'blockquote',

    # Liens
    'a',

    # Tableaux
    'table', 'thead', 'tbody',
    'tr', 'th', 'td',
])


ALLOWED_ATTRS = {
    '*': [
        'style',
        'class',
    ],
    'a': [
        'href',
        'title',
        'target',
        'rel',
    ],
    'td': [
        'colspan',
        'rowspan',
        'style',
    ],
    'th': [
        'colspan',
        'rowspan',
        'style',
    ],
    'table': [
        'style',
        'border',
        'cellpadding',
        'cellspacing',
    ],
}

css_sanitizer = CSSSanitizer(
    allowed_css_properties=ALLOWED_CSS_PROPERTIES
)

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            clean_html = bleach.clean(
                data['content_html'],
                tags=ALLOWED_TAGS,
                # attributes=ALLOWED_ATTRS
            )

            with transaction.atomic():
                message = Message.objects.create(
                    sender=request.user,
                    subject=data['subject'],
                    content_html=clean_html
                )
                emails = form.cleaned_data.get('target_departement')
                
                print("Emails to send:", form.data.get('target_departement'))
                # if data['target_type'] == 'user':
                #     MessageRecipient.objects.create(
                #         message=message,
                #         recipient=data['target_user']
                #     )
                # else:
                #     users = data['target_department'].users.exclude(
                #         id=request.user.id
                #     )
                #     MessageRecipient.objects.bulk_create([
                #         MessageRecipient(message=message, recipient=u)
                #         for u in users
                #     ])

            return render(request, 'messages/send.html', {'form': form})
    else:
        form = MessageForm()

    return render(request, 'messages/send.html', {'form': form})

class SendFormview(FormView):
    template_name = "messages/send.html"
    form_class = MessageForm
    success_url = reverse_lazy("send_message")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = list(self.request.user.get_all_permissions())
        return context
    

    def form_valid(self, form):
        data = form.cleaned_data

        clean_html = bleach.clean(
            data['content_html'],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRS,
             css_sanitizer=css_sanitizer,
            strip=True
        )

        departement=Departements.objects.get(name=data['departement'])
        with transaction.atomic():
            message = Message.objects.create(
                sender=self.request.user,
                subject=data['subject'],
                departement = departement,
                content_html=clean_html
            )
            emails = User.objects.filter(
                is_active=True,
                profil_employee__departement_id=departement
            ).exclude(email__isnull=True).exclude(email="").values_list('email', flat=True)
            #send emails
            html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>{message.subject}</title>
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
                                background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
                                color: white;
                                padding: 30px;
                                text-align: center;
                            }}
                            .header h1 {{
                                margin: 0;
                                font-size: 26px;
                            }}
                            .content {{
                                padding: 30px;
                            }}
                            .footer {{
                                background: #343a40;
                                color: white;
                                text-align: center;
                                padding: 20px;
                                font-size: 14px;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="email-container">
                            <div class="header">
                                <h1>{message.subject}</h1>
                                <p>Message du département {message.departement.name}</p>
                            </div>

                            <div class="content">
                                {message.content_html}
                            </div>

                            <div class="footer">
                                <p><strong>L'équipe RH - Parinari</strong></p>
                                <p>© 2025 Parinari. Tous droits réservés.</p>
                                <p>Contact : parinari2025@gmail.com</p>
                            </div>
                        </div>
                    </body>
                    </html>
                    """
                    
            print("HTML Content:", html_content);

            from django.core.mail import EmailMultiAlternatives
            from django.conf import settings

            email = EmailMultiAlternatives(
                subject=message.subject,
                body="This is an important message.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=list(emails),
            )

            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=True)
            #bluck create notification
            Notification.objects.bulk_create([
                Notification(
                    to=user,
                    title=f"Nouveau message dans le département {departement.name}",
                    content="Vous avez reçu un nouveau message. Consultez vos mails",
                )
                for user in User.objects.filter(
                    is_active=True,
                    profil_employee__departement_id=departement.id
                )
            ])
            
            # print("Emails to send:", list(emails))


        return super().form_valid(form)
    
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def notifications_list(request):
    notifications = request.user.notifications.all()
    return render(request, "messages/notifications.html", {
        "notifications": notifications,
        "permissions": list(request.user.get_all_permissions()),
    })

from django.shortcuts import redirect, get_object_or_404

@login_required
def mark_notification_read(request, pk):
    notif = get_object_or_404(
        Notification, pk=pk, to=request.user
    )
    notif.is_read = True
    notif.save(update_fields=["is_read"])
    return redirect(request.META.get("HTTP_REFERER", "/"))
