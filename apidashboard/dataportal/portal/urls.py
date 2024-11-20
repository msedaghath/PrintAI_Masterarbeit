from django.urls import path

from .views import IndexView, LoginView, logoutUser, SignUpView, UserAccountView, CheckStyle
from .printer_views import PrinterListView, PrinterUpdateView, delete_printer, printer_detail, ControlPrinterView, PingPrinterView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('printers/', PrinterListView.as_view(), name='printer_list'),
    path('printers/edit/<int:pk>', PrinterUpdateView.as_view(), name='edit_printer'),
    path('printers/delete/<int:printer_id>', delete_printer, name='delete_printer'),
    path('printers/<int:pk>', printer_detail, name='printer_detail'),
    path('printers/control/<int:printer_id>', ControlPrinterView.as_view(), name='control_printer'),
    path('printers/ping/<int:printer_id>', PingPrinterView.as_view(), name='ping_printer'),
    path('login', LoginView.as_view(), name='login'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout', logoutUser, name='logout'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('user_account', UserAccountView.as_view(), name='user_account'),
    path('check', CheckStyle.as_view(), name='check')
]
