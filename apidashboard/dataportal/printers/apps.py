from django.apps import AppConfig

class PrintersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'printers'
    verbose_name = 'Printer Management'
    
    def ready(self):
        # Import any signals here if needed
        pass