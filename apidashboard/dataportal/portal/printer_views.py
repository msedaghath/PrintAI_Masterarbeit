from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

import requests
from .forms import PrinterForm
from .models import Printer , Profile
from octorest import OctoRest
import logging 



@method_decorator(login_required(login_url='login'), name='dispatch')
class PingPrinterView(View):
    def get(self, request, *args, **kwargs):
        printer_id = kwargs.get('printer_id')
        printer = Printer.objects.get(id=printer_id)
        # url = f"http://{printer.ip_address}"
        if "http://" in printer.ip_address or "https://" in printer.ip_address:
            url = printer.ip_address
        else:
            url = f"http://{printer.ip_address}"
        apikey = printer.api_key
        try:
            client = OctoRest(url=url, apikey=apikey)
            client.printer()['state']['flags']['ready']
            print(client.printer()['state']['flags']['ready'])
            printer.ping = True
            printer.save()

        except Exception as e:
            print(type(e))
            printer.ping = False
            printer.save()
        return redirect('printer_list')

class PrinterListView(LoginRequiredMixin, ListView, FormMixin):
    model = Printer
    context_object_name = 'printers'
    template_name = 'portal/printer_pages/printer_list.html'
    form_class = PrinterForm

    def get_queryset(self):
        # Assuming 'user' attribute in Profile model points to Django's User model
        user_profile, created = Profile.objects.get_or_create(user=self.request.user)
        return Printer.objects.filter(profile=user_profile)

    def get(self, request, *args, **kwargs):
        self.object = None
        self.object_list = self.get_queryset()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form, object_list=self.object_list))

    def post(self, request, *args, **kwargs):
        self.object = None
        self.object_list = self.get_queryset()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            # Ensure that the printer is associated with the current user's profile
            printer = form.save(commit=False)
            printer.profile = Profile.objects.get(user=request.user)
            printer.save()
            return redirect('printer_list')
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        try:
            # form.save() is now handled in the post method to associate the printer with the user's profile
            return redirect('printer_list')
        except IntegrityError:
            form.add_error(None, "A printer with this IP and API Key already exists.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, object_list=self.object_list))

# class PrinterListView(LoginRequiredMixin, ListView, FormMixin):
#     model = Printer
#     context_object_name = 'printers'
#     template_name = 'portal/printer_pages/printer_list.html'
#     form_class = PrinterForm

#     def get(self, request, *args, **kwargs):
#         self.object = None
#         self.object_list = self.get_queryset()
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         return self.render_to_response(self.get_context_data(form=form, object_list=self.object_list))

#     def post(self, request, *args, **kwargs):
#         self.object = None
#         self.object_list = self.get_queryset()
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_valid(self, form):
#         try:
#             form.save()
#             return redirect('printer_list')
#         except IntegrityError:
#             form.add_error(None, "A printer with this IP and API Key already exists.")
#             return self.form_invalid(form)

#     def form_invalid(self, form):
#         return self.render_to_response(self.get_context_data(form=form, object_list=self.object_list))

class PrinterUpdateView(LoginRequiredMixin, UpdateView):
    model = Printer
    form_class = PrinterForm
    template_name = 'portal/printer_pages/printer_add.html'
    success_url = reverse_lazy('printer_list')


# @login_required(login_url='login')
# def printer_detail(request, pk):

#     printer = Printer.objects.get(pk=pk)
#     # url = f"http://{printer.ip_address}"
#     if "http://" in printer.ip_address or "https://" in printer.ip_address:
#         url = printer.ip_address
#     else:
#         url = f"http://{printer.ip_address}"
#     apikey = printer.api_key
#     print(url) 
#     # Assign default values before the try block
#     printer_info = None
#     temperature_history = None
#     current_temperature = None

#     try:
#         client = OctoRest(url=url, apikey=apikey)
#         printer_info = get_printer_info(client)
#         # temperature_history = get_temperature_history(client)
#         # current_temperature = get_current_temperature(client)
#     except Exception as e:
#         print (e , 'error in the try block')

#     context = {
#         'printer': printer,
#         'printer_info': printer_info,
#         'temperature_history': temperature_history,
#         'current_temperature': current_temperature,
#     }
#     return render(request, 'portal/printer_pages/printer_detail.html', context)


#     def get_printer_info(client):
#         try:
#             response = client.printer()

#             if response.status_code != 200:
#                 raise Exception(f"Error: Received status code {response.status_code}")

#             data = response.json()  # Assumes the response is JSON

#             # Validate the response data (replace with your actual validation logic)
#             if 'expected_field' not in data:
#                 raise Exception("Invalid response data")

#             # Extract the data you're interested in
#             printer_info = data['expected_field']

#             return printer_info
#         except Exception as e:
#             logging.error(f"Failed to get printer info: {e}")
#             raise

#     def get_temperature_history(client):

#         try:
#             response = client.history()

#             if response.status_code != 200:
#                 raise Exception(f"Error: Received status code {response.status_code}")

#             data = response.json()  # Assumes the response is JSON

#             # Validate the response data (replace with your actual validation logic)
#             if 'expected_field' not in data:
#                 raise Exception("Invalid response data")

#             # Extract the data you're interested in
#             temperature_history = data['expected_field']

#             return temperature_history
#         except Exception as e:
#             logging.error(f"Failed to get temperature history: {e}")
#             raise

#     def get_current_temperature(client):
#         try:
#             response = client.temperature()

#             if response.status_code != 200:
#                 raise Exception(f"Error: Received status code {response.status_code}")

#             data = response.json()  # Assumes the response is JSON

#             # Validate the response data (replace with your actual validation logic)
#             if 'expected_field' not in data:
#                 raise Exception("Invalid response data")

#             # Extract the data you're interested in
#             current_temperature = data['expected_field']

#             return current_temperature
#         except Exception as e:
#             logging.error(f"Failed to get current temperature: {e}")
#             raise


@login_required(login_url='login')
def delete_printer(request, printer_id):
    #printer = Printer.objects.get(id=printer_id)
    printer = get_object_or_404(Printer, id=printer_id)
    printer.delete()
    return redirect('printer_list')

class ControlPrinterView(LoginRequiredMixin, View):
    template_name = 'portal/printer_pages/control_printer.html'

    def get(self, request, *args, **kwargs):
        printer_id = kwargs.get('printer_id')
        printer = Printer.objects.get(id=printer_id)
        # url = f"http://{printer.ip_address}"
        if "http://" in printer.ip_address or "https://" in printer.ip_address:
            url = printer.ip_address
        else:
            url = f"http://{printer.ip_address}"
        apikey = printer.api_key
        
        files = []  # Initialize files as an empty list

        try:
            client = OctoRest(url=url, apikey=apikey)
            file_list = client.files()['files']  # Get the list of files in the local storage of Octoprint
            files = [file['display'] for file in file_list]  # Extract the filenames from the file list
            printer.ping = True
        except Exception as e:
            print(e)
            printer.ping = False
        finally:
            printer.save()

        return render(request, self.template_name, {"printer": printer, "files": files})

    def post(self, request, *args, **kwargs):
        printer_id = kwargs.get('printer_id')
        printer = Printer.objects.get(id=printer_id)
        url = f"http://{printer.ip_address}"
        apikey = printer.api_key
        client = OctoRest(url=url, apikey=apikey)

        command = request.POST.get('command')
        print(command)
        if command == 'home':
            # Home the printer
            try:
                client.home()
            except Exception as e:
                print(e)
        elif command == 'pause':
            try:
                client.pause()
            except Exception as e:
                print(e)
        elif command == 'resume':
            try:
                client.resume()
            except Exception as e:
                print(e)
        elif command == 'cancel':
            try: 
                client.cancel()
            except Exception as e:
                print(e)
        elif command == 'start':
            try:
                client.start()
            except Exception as e:
                print(e)
        elif command == 'restart':
            try:
                client.restart()
            except Exception as e:
                print(e)
        elif command == 'upload':
            gcode_file = request.FILES.get('gcode')
            # Upload the gcode file
            if gcode_file:
                try:
                    client.files.upload(gcode_file.temporary_file_path())
                except Exception as e:
                    print(e)
        elif command == 'shutdown':
            try:
                client.execute_system_command(source='core', action='shutdown')
            except Exception as e:
                print(e)

        # Redirect to the same page after handling the form data
        return HttpResponseRedirect(request.path_info)

#Printer detail view, designated page for each printer 
@login_required(login_url='login')

# def printer_detail(request, pk):    
#     printer = Printer.objects.get(pk=pk)
#     if "http://" in printer.ip_address or "https://" in printer.ip_address:
#         url = printer.ip_address
#     else:
#         url = f"http://{printer.ip_address}"
#     apikey = printer.api_key
#     print(url) 
#     def make_client(url, apikey):
#      try:
#          client = OctoRest(url=url, apikey=apikey)
#          return client
#      except ConnectionError as ex:
#             print(ex)
    
#     def get_version():
#         try :
#             client = make_client(url,apikey)
#             message = "You are using OctoPrint v" + client.version['server'] + "\n"
#             ping_printer = True 
#             print(message , ping_printer)
#             return message 
#         except Exception as e:
#             ping_printer = False
#             return "Server is not responding"

#     def get_printer_info():
#         try:
#             client = make_client(url,apikey)
#             printer_info = ""
#             # printer_info += str(client.version) + "\n"
#             # printer_info += str(client.job_info()) + "\n"
#             printing = client.printer()['state']['flags']['printing']
                                  
#             if printing:
#                 printer_info += "Currently printing!\n"
#             else:
#                 printer_info += "Not currently printing...\n"
#             return printer_info
#         except Exception as e:
#             print(e)
#     def get_temprature_history():
#         try:
#             client = make_client(url,apikey)
#             temprature_history = client.printer(history=True)
#             temprature_history = temprature_history['temperature']['tool0']['actual']
#             print(temprature_history)
#             # add to the list to temp history
            
#             lis = (list(temprature_history))
            
#             print(lis)
#             return temprature_history
#         except Exception as e:
#             print(e)
#     def get_current_temprature():
#         try:
#             client = make_client(url,apikey)
#             current_temprature = client.printer()
#             current_temprature_tool = current_temprature['temperature']['tool0']['actual']
#             current_temprature_bed = current_temprature['temperature']['bed']['actual']
#             current_temprature_list = {'c_tool' : current_temprature_tool , 'c_bed' : current_temprature_bed}   
#             return current_temprature_list
#         except Exception as e:
#             print(e)

#     def run_thefunctions():

#         pass
        
#     if request.method == 'GET':
#         get_version()
#         get_printer_info()
#         get_temprature_history()
#         get_current_temprature()
#     if request.method == 'POST':
#         run_thefunctions()
#     # add printer info to the context 
#     context = {'message' : get_version ,
#      'printer': printer ,  
#      'printer_info' : get_printer_info,
#     'print_history' : get_temprature_history,
#     'current_temprature' : get_current_temprature,
#      }
#     return render(request, 'portal/printer_pages/printer_detail.html', context)
#     return render(request, 'portal/printer_pages/printer_detail.html', context)

def printer_detail(request, pk):    
    printer = Printer.objects.get(pk=pk)

    if "http://" in printer.ip_address or "https://" in printer.ip_address:
        url = printer.ip_address
    else:
        url = f"http://{printer.ip_address}"

    apikey = printer.api_key
    client = OctoRest(url=url, apikey=apikey)  # Create a client once

    def get_version():
        try:
            message = "You are using OctoPrint v" + client.version['server']
            return message, True
        except Exception as e:
            return "Server is not responding", False

    def get_printer_info():
        try:
            printing = client.printer()['state']['flags']['printing']
            return "Currently printing!" if printing else "Not currently printing..."
        except Exception as e:
            return str(e)

    def get_temprature_history():
        try:
            temperature_history = client.printer(history=True)
            return temperature_history['temperature']['tool0']['actual']
        except Exception as e:
            return [str(e)]

    def get_current_temprature():
        try:
            current_temprature = client.printer()
            return {
                'c_tool': current_temprature['temperature']['tool0']['actual'],
                'c_bed': current_temprature['temperature']['bed']['actual']
            }
        except Exception as e:
            return {"error": str(e)}

    # Execute functions and retrieve results
    message, ping_printer = get_version()
    printer_info = get_printer_info()
    temperature_history = get_temprature_history()
    current_temperature = get_current_temprature()

    context = {
        'message': message,
        'printer': printer,
        'printer_info': printer_info,
        'print_history': temperature_history,
        'current_temperature': current_temperature,
        'ping_printer': ping_printer
    }

    return render(request, 'portal/printer_pages/printer_detail.html', context)
