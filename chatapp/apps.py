from django.apps import AppConfig


class ChatappConfig(AppConfig):
    name = 'chatapp'

    def ready(self):
        import chatapp.signals