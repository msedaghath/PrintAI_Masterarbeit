from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Printer
from accounts.models import Profile
from .services import PrinterService, MonitoringService
from .forms import PrinterForm

class PrinterListView(LoginRequiredMixin, ListView, FormMixin):
    """View for listing all printers and adding new ones"""
    model = Printer
    context_object_name = 'printers'
    template_name = 'printers/printer_list.html'
    form_class = PrinterForm
    login_url = 'login'

    def get_queryset(self):
        user_profile, created = Profile.objects.get_or_create(user=self.request.user)
        return Printer.objects.filter(profile=user_profile)

    def get(self, request, *args, **kwargs):
        self.object = None
        self.object_list = self.get_queryset()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = None
        self.object_list = self.get_queryset()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            # Ensure that the printer is associated with the current user's profile
            printer = form.save(commit=False)
            printer.profile = Profile.objects.get(user=request.user)
            try:
                printer.save()
                return redirect('printer_list')
            except IntegrityError:
                form.add_error(None, "A printer with this IP and API Key already exists.")
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class PrinterUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating printer information"""
    model = Printer
    form_class = PrinterForm
    template_name = 'printers/printer_update.html'
    success_url = reverse_lazy('printer_list')
    login_url = 'login'


class PrinterDetailView(LoginRequiredMixin, DetailView):
    """View for displaying detailed information about a printer"""
    model = Printer
    context_object_name = 'printer'
    template_name = 'printers/printer_detail.html'
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        printer = self.object
        
        # Get printer status
        status = PrinterService.get_printer_status(printer)
        context['printer_status'] = status
        
        # Check if there was an error getting the status
        if 'error' in status:
            context['message'] = f"Error: {status['error']}"
            context['ping_printer'] = False
        else:
            context['message'] = f"You are using OctoPrint v{status['version']}"
            context['printer_info'] = "Currently printing!" if status['is_printing'] else "Not currently printing..."
            context['current_temperature'] = {
                'c_tool': status['temperature']['tool0']['actual'] if 'tool0' in status['temperature'] else 'N/A',
                'c_bed': status['temperature']['bed']['actual'] if 'bed' in status['temperature'] else 'N/A'
            }
            context['ping_printer'] = True
            
            # Get temperature history for charting
            try:
                temperature_history = PrinterService.get_client(printer).printer(history=True)
                context['print_history'] = temperature_history['temperature']['tool0']['actual']
            except Exception:
                context['print_history'] = []
        
        # Get last print data from monitoring
        context['last_print_data'] = MonitoringService.get_last_print_data(printer)
        
        return context


@login_required(login_url='login')
def delete_printer(request, printer_id):
    """Delete a printer"""
    printer = get_object_or_404(Printer, id=printer_id)
    
    # Verify that the printer belongs to the current user
    user_profile = Profile.objects.get(user=request.user)
    if printer.profile != user_profile:
        return HttpResponse("Unauthorized", status=403)
        
    printer.delete()
    return redirect('printer_list')


class PingPrinterView(LoginRequiredMixin, View):
    """View for pinging a printer to check if it's online"""
    login_url = 'login'
    
    def get(self, request, *args, **kwargs):
        printer_id = kwargs.get('printer_id')
        printer = get_object_or_404(Printer, id=printer_id)
        
        # Verify that the printer belongs to the current user
        user_profile = Profile.objects.get(user=request.user)
        if printer.profile != user_profile:
            return HttpResponse("Unauthorized", status=403)
            
        success = PrinterService.ping_printer(printer)
        return redirect('printer_list')


class ControlPrinterView(LoginRequiredMixin, View):
    """View for controlling printer operations"""
    template_name = 'printers/control_printer.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        printer_id = kwargs.get('printer_id')
        printer = get_object_or_404(Printer, id=printer_id)
        
        # Verify that the printer belongs to the current user
        user_profile = Profile.objects.get(user=request.user)
        if printer.profile != user_profile:
            return HttpResponse("Unauthorized", status=403)
        
        files = []
        try:
            files = [file['name'] for file in PrinterService.get_printer_files(printer)]
            printer.ping = True
        except Exception:
            printer.ping = False
        finally:
            printer.save()

        return render(request, self.template_name, {"printer": printer, "files": files})

    def post(self, request, *args, **kwargs):
        printer_id = kwargs.get('printer_id')
        printer = get_object_or_404(Printer, id=printer_id)
        
        # Verify that the printer belongs to the current user
        user_profile = Profile.objects.get(user=request.user)
        if printer.profile != user_profile:
            return HttpResponse("Unauthorized", status=403)
            
        command = request.POST.get('command')
        
        # For file uploads
        file_arg = {}
        if command == 'upload' and 'gcode' in request.FILES:
            file_arg = {'file': request.FILES['gcode']}
            
        # Send the command to the printer
        success = PrinterService.send_printer_command(printer, command, **file_arg)
        
        # Redirect to the same page after handling the form data
        return HttpResponseRedirect(request.path_info)


class WebcamStreamView(LoginRequiredMixin, View):
    """View for streaming webcam feed from the printer"""
    login_url = 'login'
    
    def get(self, request, printer_id):
        printer = get_object_or_404(Printer, id=printer_id)
        
        # Verify that the printer belongs to the current user
        user_profile = Profile.objects.get(user=request.user)
        if printer.profile != user_profile:
            return HttpResponse("Unauthorized", status=403)
            
        ip_address = printer.ip_address
        if not ip_address.startswith(('http://', 'https://')):
            ip_address = f'http://{ip_address}'
        stream_url = f"{ip_address}/webcam/?action=stream"

        try:
            import requests
            response = requests.get(stream_url, stream=True)
            return HttpResponse(
                response.raw,
                content_type=response.headers.get('Content-Type', 'multipart/x-mixed-replace')
            )
        except Exception:
            return HttpResponse("Unable to connect to the printer webcam.", status=502)