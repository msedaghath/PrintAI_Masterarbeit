from traceback import print_list
from django.urls import path

from .views import IndexView, LoginView, logoutUser, SignUpView , UserAccountView , CheckStyle, WebcamStreamView, user_account
from .printer_views import *
from portal.services import AlertService

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('printers/', PrinterListView.as_view(), name='printer_list'),
    # path('printers/add/', PrinterCreateView.as_view(), name='printer_add'),
    path('printers/edit/<int:pk>', PrinterUpdateView.as_view(), name='edit_printer'),
    #path('printers/delete/<int:pk>', PrinterDeleteView.as_view(), name='delete_printer'),
    path('printers/delete/<int:printer_id>', delete_printer , name= 'delete_printer'),
    path('printers/<int:pk>', printer_detail, name='printer_detail'),
    path('printers/control/<int:printer_id>', ControlPrinterView.as_view(), name='control_printer'),
    # path('printers/ping/<int:printer_id>', ping_printer, name='ping_printer'),
    path('printers/ping/<int:printer_id>', PingPrinterView.as_view(), name='ping_printer'),
    path('printer/<int:printer_id>/webcam/', WebcamStreamView.as_view(), name='webcam_stream'),
    path('printers/<int:printer_id>/export_csv', export_csv, name='export_csv'),
    path('login', LoginView.as_view(), name='login'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout', logoutUser, name='logout'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('user_account', UserAccountView.as_view(), name='user_account'),
    path('check', CheckStyle.as_view(), name='check' ),
    path('account/', user_account, name='user_account'),
    path('webhook/alert/', AlertService.handle_alert, name='alert_webhook'),

]
