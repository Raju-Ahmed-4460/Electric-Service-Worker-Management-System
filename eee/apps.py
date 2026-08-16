from django.apps import AppConfig


class EeeConfig(AppConfig):

    default_auto_field = "django.db.models.BigAutoField"

    name = "eee"

    def ready(self):
        import eee.signals