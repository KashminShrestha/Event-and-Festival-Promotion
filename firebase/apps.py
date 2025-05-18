from django.apps import AppConfig


class FirebaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'firebase'
    
    def ready(self):
        import firebase.signals