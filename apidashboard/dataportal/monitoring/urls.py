from django.urls import path
from . import views

urlpatterns = [
    path('export-csv/<int:printer_id>/', views.export_csv, name='export_csv'),
]