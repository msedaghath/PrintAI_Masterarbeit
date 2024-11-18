from traceback import print_list
from django.urls import path

from .views import IndexView, LoginView, logoutUser, SignUpView , UserAccountView , CheckStyle


# urlpatterns = [
#     path('', views.index , name='index'),
#     # path('data', data_print),
#     # path('data/<int:data_id>', data_print),
#     #path('printer', printer_add),
#     path('printers/', print_list, name='printer_list'),
#     # path('printers/delete/<int:printer_id>', delete_printer , name= 'delete_printer'),
#     path('printers/edit/<int:printer_id>', edit_printer, name='edit_printer'),
#     path('printers/<int:printer_id>', printer_detail, name='printer_detail'),
#     path('printers/ping/<int:printer_id>', ping_printer, name='ping_printer'),
#     path('login', views.loginPage, name='login'),
#     path('logout', views.logoutUser, name='logout'),
#     path('signup', views.signupPage, name='signup'),
# ]

from django.urls import path

# from .views import IndexView, LoginView, logoutUser, SignUpView ,PrinterCreateView  ,PrinterDeleteView
from .printer_views import *

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
    path('login', LoginView.as_view(), name='login'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout', logoutUser, name='logout'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('user_account', UserAccountView.as_view(), name='user_account'),
    path('check', CheckStyle.as_view(), name='check' )
]
