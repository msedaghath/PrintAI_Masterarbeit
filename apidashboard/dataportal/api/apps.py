from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = 'API Endpoints'
    
    def ready(self):
        # Import any signals here if needed
        pass