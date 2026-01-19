from django.apps import AppConfig


class CongesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'conges'

    #add signals
    def ready(self):
        import conges.signals