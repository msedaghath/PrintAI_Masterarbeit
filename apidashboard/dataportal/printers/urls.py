from django.urls import path
from . import views

urlpatterns = [
    path('', views.PrinterListView.as_view(), name='printer_list'),
    path('update/<int:pk>/', views.PrinterUpdateView.as_view(), name='printer_update'),
    path('detail/<int:pk>/', views.PrinterDetailView.as_view(), name='printer_detail'),
    path('delete/<int:printer_id>/', views.delete_printer, name='delete_printer'),
    path('ping/<int:printer_id>/', views.PingPrinterView.as_view(), name='ping_printer'),
    path('control/<int:printer_id>/', views.ControlPrinterView.as_view(), name='control_printer'),
    path('webcam/<int:printer_id>/', views.WebcamStreamView.as_view(), name='webcam_stream'),
]