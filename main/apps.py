from django.apps import AppConfig
from watson import search as watson

class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        Apk = self.get_model ("Apk")
        watson.register (Apk)
