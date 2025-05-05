from django.urls import path
from . import views

urlpatterns = [
    path('alert/', views.handle_alert, name='handle_alert'),
    path('printer/<int:printer_id>/status/', views.printer_status_update, name='printer_status_update'),
]