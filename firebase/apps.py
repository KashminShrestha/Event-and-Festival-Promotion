from django.apps import AppConfig

class FirebaseConfig(AppConfig):
    name = 'firebase'

    def ready(self):
        import firebase.signals

