from .models import Notification

def notify_user(*, user, title, content, link):
    """
    Création centralisée d'une notification
    """
    return Notification.objects.create(
        to=user,
        title=title,
        content=content,
        link=link
    )
