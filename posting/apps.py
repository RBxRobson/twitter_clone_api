from django.apps import AppConfig

class PostingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posting'

    def ready(self):
        import posting.signals
