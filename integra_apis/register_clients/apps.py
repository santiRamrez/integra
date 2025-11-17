from django.apps import AppConfig


class RegisterClientsConfig(AppConfig):
    default_auto_field = "django_mongodb_backend.fields.ObjectIdAutoField"
    name = "register_clients"

    def ready(self):
        import register_clients.signals
