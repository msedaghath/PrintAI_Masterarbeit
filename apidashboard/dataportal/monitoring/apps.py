from django.apps import AppConfig

class MonitoringConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monitoring'
    verbose_name = 'Printer Monitoring'
    
    def ready(self):
        # Import any signals here if needed
        pass