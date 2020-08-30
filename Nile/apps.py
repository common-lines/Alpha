from django.apps import AppConfig


class NileConfig(AppConfig):
    name = 'Nile'

    def ready(self):
        import Nile.signals
